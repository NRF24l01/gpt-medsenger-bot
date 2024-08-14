import json
from flask import Flask, request, render_template, redirect, url_for, jsonify
from config import *
from medsenger_api import *
from celery import Celery, Task
import time
from markdown2 import Markdown
from tasks import ask_yai, ask_cai, change_cai
from helper import get_model, get_prompt

app = Flask(__name__)
medsenger_api = AgentApiClient(APP_KEY, MAIN_HOST, debug=True)

with open("contract_model.json", "r", encoding="utf-8") as f:
    contract_model = json.loads(f.read())

with open("models.json", "r", encoding="utf-8") as f:
    models = json.loads(f.read())

with open("contract_prompts.json", "r", encoding="utf-8") as f:
    prompts = json.loads(f.read())

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
    contract_model, cmodel = get_model(request.args.get('contract_id'), contract_model, CHATGPT_BASIC)
    print(cmodel)
    return render_template('settings.html', models=models, cmodel=cmodel, coid=request.args.get('contract_id'), prompt=get_prompt(request.args.get('contract_id'), prompts, bprompt)[1])


@app.route("/settings", methods=['POST'])
def update_model():
    global models, contract_model, prompts
    get_model(request.form.get("coid"), contract_model, CHATGPT_BASIC)
    with open("contract_model.json", "r", encoding="utf-8") as f:
        contract_model = json.loads(f.read())

    contract_model[request.form.get("coid")] = request.form.get("selselsel")

    with open("contract_model.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(contract_model))

    with open("contract_prompts.json", "r", encoding="utf-8") as f:
        prompts = json.loads(f.read())

    prompts[request.form.get("coid")] = request.form.get("prompt")

    with open("contract_prompts.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(prompts))

    print(request.form.get("selselsel"))
    print(request.form.get("coid"))

    change_prompt_cai.delay(request.form.get("coid"), request.form.get("prompt"))
    change_cai.delay(request.form.get("coid"), models[contract_model[request.form.get("coid")]]["name"])

    return "<script>window.parent.postMessage('close-modal-success','*');</script>"


@app.route('/', methods=['GET'])
def index():
    return 'waiting for the Ithunder!'


@app.route('/message', methods=['POST'])
def save_message():
    global models, contract_model
    print(request.json)
    # medsenger_api.send_message(request.json["contract_id"], "asked")
    with open("contract_model.json", "r", encoding="utf-8") as f:
        contract_model = json.loads(f.read())

    if AITYPE == 1:
        ask_yai.delay(request.json, request.json["message"]["text"])
    elif AITYPE == 2:
        change_cai.delay(str(request.form.get("coid")), models[get_model(str(request.json["contract_id"]), contract_model, CHATGPT_BASIC)[1]]["name"])
        ask_cai.delay(request.json, request.json["message"]["text"])
    return "ok"


if __name__ == "__main__":
    app.run(port=PORT, host=HOST, debug=True)
