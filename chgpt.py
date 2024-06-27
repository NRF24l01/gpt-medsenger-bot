import requests
from json import loads
from time import time
from config import MAX_SESSION_TIME, MAX_DOCTOR_TIME, CHATGPT_HOST, CHATGPT_KEY, CHATGPT_MODEL


class ChGPT:
    def __init__(self, api_key: str, url: str, model: str, prompt: str = False):
        self.token = api_key
        self.url = url
        self.prompt = prompt
        self.model = model
        self.messages = []

        if not prompt:
            with open("prompt.txt", "r", encoding="UTF-8") as f:
                self.set_prompt(f.read())

        self.messages.append({"role": "system", "content": self.prompt})

    def set_prompt(self, prompt: str):
        self.prompt = prompt

    def send_request(self, context: dict):
        response = requests.post(self.url, json=context)
        return response.text

    def ask_model(self, question):
        self.messages.append({"role": "user", "content": question})
        print(self.messages)
        payload = {"token": self.token,
                   "model": self.model,
                   "context": self.messages}
        ans = loads(self.send_request(payload))
        print(ans)
        self.messages.append(ans["result"]["choices"][0]["message"])
        return ans


class ManyCGPT(ChGPT):
    def __init__(self, api_key: str, url: str, model: str, prompt: str = False):
        super().__init__(api_key, url, model, prompt)
        self.agents = {}

    def new_agent(self, contract_id):
        self.agents[contract_id] = {"start_time": time(), "last_time": time(), "last_doc_time": 0,
                                    "gpt": ChGPT(CHATGPT_KEY, CHATGPT_HOST, CHATGPT_MODEL)}

    def clear_context(self, contract_id):
        self.agents[contract_id] = {"start_time": time(), "last_time": time(), "last_doc_time": 0,
                                    "gpt": ChGPT(CHATGPT_KEY, CHATGPT_HOST, CHATGPT_MODEL)}

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


if __name__ == "__main__":
    gpt = ManyCGPT(CHATGPT_KEY, CHATGPT_HOST, CHATGPT_MODEL)
    print(gpt.ask("1111", "ЭЭЭ у меня башка балит"))
    print(gpt.ask("1111", "А что мне тогида делать?"))
