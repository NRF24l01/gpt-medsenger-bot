import json
from flask import Flask, request, render_template
from config import *
from medsenger_api import *
from yagpt import YaGPT, ManyYGPT
from celery import Celery, Task
import time
from markdown2 import Markdown
from tasks import ask_yai, ask_cai

app = Flask(__name__)
medsenger_api = AgentApiClient(APP_KEY, MAIN_HOST, debug=True)


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
    return render_template('settings.html')


@app.route('/', methods=['GET'])
def index():
    return 'waiting for the thunder!'


@app.route('/message', methods=['POST'])
def save_message():
    print(request.json)
    # medsenger_api.send_message(request.json["contract_id"], "asked")

    if AITYPE == 1:
        ask_yai.delay(request.json, request.json["message"]["text"])
    elif AITYPE == 2:
        ask_cai.delay(request.json, request.json["message"]["text"])
    return "ok"


if __name__ == "__main__":
    app.run(port=PORT, host=HOST, debug=True)
