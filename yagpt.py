import requests
from json import loads
from time import time
from config import MAX_SESSION_TIME, MAX_DOCTOR_TIME


class YaGPT:
    def __init__(self, dir_id: str, api_key: str, prompt: str = False,
                 url: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"):
        self.dir_id = dir_id
        self.api_key = api_key
        self.url = url
        self.prompt = prompt
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key " + self.api_key
        }
        self.messages = []

        if not prompt:
            with open("prompt.txt", "r", encoding="UTF-8") as f:
                self.set_prompt(f.read())

        self.messages.append({"role": "system", "text": self.prompt})

    def set_prompt(self, prompt: str):
        self.prompt = prompt

    def send_request(self, context: dict):
        response = requests.post(self.url, headers=self.headers, json=context)
        return response.text

    def ask_model(self, question):
        self.messages.append({"role": "user", "text": question})
        payload = {"modelUri": "gpt://b1g7p0kad01qi681gqps/yandexgpt-lite",
                   "completionOptions": {
                       "stream": False,
                       "temperature": 0.6,
                       "maxTokens": "2000"
                   },
                   "messages": self.messages}
        ans = loads(self.send_request(payload))
        print(ans)
        self.messages.append(ans["result"]["alternatives"][0]["message"])
        return ans


class ManyYGPT(YaGPT):
    def __init__(self, dir_id: str, api_key: str, prompt: str = False,
                 url: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"):
        super().__init__(dir_id, api_key, prompt, url)
        self.agents = {}

    def new_agent(self, contract_id):
        self.agents[contract_id] = {"start_time": time(), "last_time": time(), "last_doc_time": 0,
                                    "gpt": YaGPT(dir_id=self.dir_id, api_key=self.api_key, prompt=self.prompt)}

    def clear_context(self, contract_id):
        self.agents[contract_id] = {"start_time": time(), "last_time": time(), "last_doc_time": 0,
                                    "gpt": YaGPT(dir_id=self.dir_id, api_key=self.api_key, prompt=self.prompt)}

    def doc(self, contract_id):
        self.agents[contract_id]["last_doc_time"] = time()

    def is_dop_dop(self, contract_id):
        if contract_id not in self.agents.keys():
            return False
        if time() - self.agents[contract_id]["last_doc_time"] < MAX_DOCTOR_TIME:
            return True
        return False

    def ask(self, contract_id, question):
        callback = "cont"
        if contract_id not in self.agents.keys():
            self.new_agent(contract_id)
            callback = "new"
        elif self.agents[contract_id] == 0:
            self.new_agent(contract_id)
            callback = "new"
        elif time() - self.agents[contract_id]["last_time"] > MAX_SESSION_TIME:
            self.new_agent(contract_id)
            callback = "new"
        elif time() - self.agents[contract_id]["last_doc_time"] < MAX_DOCTOR_TIME:
            return {}, "dop"
        res = self.agents[contract_id]["gpt"].ask_model(question)
        self.agents[contract_id]["last_time"] = time()

        return res, callback
