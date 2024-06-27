import json
from flask import Flask, request, render_template
from config import *
from medsenger_api import *
from yagpt import YaGPT, ManyYGPT
from chgpt import ManyCGPT
from celery import Celery, Task
import time
from markdown2 import Markdown
from infrastructure import celery

ygpt = ManyYGPT(DIR_ID, API_KEY)
cgpt = ManyCGPT(CHATGPT_KEY, CHATGPT_HOST, CHATGPT_MODEL)
markdowner = Markdown()


@celery.task
def ask_yai(json: dict, txt: str) -> str:
    if json["message"]["sender"] == "doctor":
        ygpt.clear_context(json["contract_id"])
        ygpt.doc(json["contract_id"])
        return "ok"

    medsenger_api = AgentApiClient(APP_KEY, MAIN_HOST, debug=True)
    if ygpt.is_dop_dop(json["contract_id"]):
        return 1
    medsenger_api.send_message(json["contract_id"], "Запрос отправлен. Ожидаем ответ.", forward_to_doctor=False)

    ans, callback = ygpt.ask(json["contract_id"], txt)
    print(ans, callback)
    ai_ans = ans['result']['alternatives'][0]['message']['text']

    if callback == "cont":
        text = f"_Продолжение диалога._\n # Внимание! Ответ создан нейросетью, будьте осторожны, не принимайте всё за чистую монету!!\n{ai_ans}"
    elif callback == "new":
        text = f"_Новый диалог._\n # Внимание! Ответ создан нейросетью, будьте осторожны, не принимайте всё за чистую монету!!\n{ai_ans}"
    else:
        text = "# Что-то пошло не так."
    html_ans = markdowner.convert(text).replace('\n', '')
    medsenger_api.send_message(json["contract_id"], html_ans, forward_to_doctor=False)
    return 1


@celery.task
def ask_cai(json: dict, txt: str) -> str:
    if json["message"]["sender"] == "doctor":
        cgpt.clear_context(json["contract_id"])
        cgpt.doc(json["contract_id"])
        return "ok"

    medsenger_api = AgentApiClient(APP_KEY, MAIN_HOST, debug=True)
    if cgpt.is_dop_dop(json["contract_id"]):
        return 1
    medsenger_api.send_message(json["contract_id"], "Запрос отправлен. Ожидаем ответ.", forward_to_doctor=False)

    ans, callback = cgpt.ask(json["contract_id"], txt)
    print(ans, callback)
    ai_ans = ans['result']['alternatives'][0]['message']['text']

    if callback == "cont":
        text = f"_Продолжение диалога._\n # Внимание! Ответ создан нейросетью, будьте осторожны, не принимайте всё за чистую монету!!\n{ai_ans}"
    elif callback == "new":
        text = f"_Новый диалог._\n # Внимание! Ответ создан нейросетью, будьте осторожны, не принимайте всё за чистую монету!!\n{ai_ans}"
    else:
        text = "# Что-то пошло не так."
    html_ans = markdowner.convert(text).replace('\n', '')
    medsenger_api.send_message(json["contract_id"], html_ans, forward_to_doctor=False)
    return 1
