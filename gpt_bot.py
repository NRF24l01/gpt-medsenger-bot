import json
from flask import Flask, request, render_template, redirect, url_for, jsonify
from config import *
from medsenger_api import *
from celery import Celery, Task
import time
from markdown2 import Markdown
from tasks import ask_yai, ask_cai, change_cai, change_prompt_cai
from manage import app, db
from models import Model, Prompt
from helpers import get_or_create

medsenger_api = AgentApiClient(APP_KEY, MAIN_HOST, debug=True)



with open("models.json", "r", encoding="utf-8") as f:
    models = json.loads(f.read())

with open("prompt.txt", "r", encoding="utf-8") as f:
    bprompt = f.read()

@app.route('/status', methods=['POST'])
def status():
    data = request.json

    if data['api_key'] != APP_KEY:
        return 'invalid key'

    answer = {
        "is_tracking_data": False,
        "supported_scenarios": [],
        "tracked_contracts": []
    }

    return json.dumps(answer)


@app.route('/init', methods=['POST'])
def init():
    data = request.json
    medsenger_api.add_record(data.get('contract_id'), 'doctor_action',
                             f'Подключен прибор "{data.get("agent_name")}".')

    return 'ok'


@app.route('/remove', methods=['POST'])
def remove():
    data = request.json

    medsenger_api.add_record(data.get('contract_id'), 'doctor_action',
                             f'Отключен прибор "{data.get("agent_name")}".')

    return 'ok'


@app.route('/settings', methods=['GET'])
def settings():
    global models, contract_model
    #print(request.args)
    modelobj = get_or_create(db.session, Model, contract_id=request.args.get('contract_id'))

    promptobj = get_or_create(db.session, Prompt, contract_id=request.args.get('contract_id'))

    cmodel = modelobj.model_name
    prompt = promptobj.prompt
    print(cmodel)
    return render_template('settings.html', models=models, cmodel=cmodel,
                           coid=request.args.get('contract_id'), prompt=prompt)


@app.route("/settings", methods=['POST'])
def update_model():
    global models

    # Change model
    modelobj = get_or_create(db.session, Model, contract_id=request.form.get("coid"))
    modelobj.model_name = request.form.get("gpt-model")
    db.session.add(modelobj)
    db.session.commit()

    # Change prompt
    promptobj = get_or_create(db.session, Prompt, contract_id=request.form.get("coid"))
    promptobj.prompt = request.form.get("prompt")
    db.session.add(promptobj)
    db.session.commit()

    # Get values
    promptobj = get_or_create(db.session, Prompt, contract_id=request.form.get("coid"))
    modelobj = get_or_create(db.session, Model, contract_id=request.form.get("coid"))

    # Set values
    change_prompt_cai.delay(request.form.get("coid"), promptobj.prompt)
    change_cai.delay(request.form.get("coid"), models[modelobj.model_name]["name"])

    return "<script>window.parent.postMessage('close-modal-success','*');</script>"


@app.route('/', methods=['GET'])
def index():
    return 'waiting for the Ithunder!'


@app.route('/message', methods=['POST'])
def save_message():
    global models
    print(request.json)

    # Get values
    promptobj = get_or_create(db.session, Prompt, contract_id=request.json["contract_id"])
    modelobj = get_or_create(db.session, Model, contract_id=request.json["contract_id"])

    # Set values
    biba = change_prompt_cai.delay(request.json["contract_id"], promptobj.prompt)
    boba = change_cai.delay(request.json["contract_id"], models[modelobj.model_name]["name"])

    biba.get()
    boba.get()

    if AITYPE == 1:
        ask_yai.delay(request.json, request.json["message"]["text"])
    elif AITYPE == 2:
        ask_cai.delay(request.json, request.json["message"]["text"])
    return "ok"


if __name__ == "__main__":
    app.run(port=PORT, host=HOST, debug=True)
