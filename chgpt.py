import requests
from json import loads, dumps
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
                self.prompt = f.read()

        self.messages.append({"role": "system", "content": self.prompt})

    def set_prompt(self, prompt: str):
        self.messages[0] = {"role": "system", "content": self.prompt}
        self.prompt = prompt

    def set_model(self, model: str):
        self.model = model

    def send_request(self, context: dict):
        response = requests.post(self.url, json=context)
        return response.text

    def ask_model(self, question):
        print(f"use model {self.model}")
        self.messages.append({"role": "user", "content": question})
        print(f"use messages {self.messages}")
        payload = {"token": self.token,
                   "model": self.model,
                   "context": self.messages}
        print("bobload " + dumps(payload))
        ans = loads(self.send_request(payload))
        print(ans)
        self.messages.append(ans["result"]["choices"][0]["message"])
        return ans


class ManyCGPT(ChGPT):
    def __init__(self, api_key: str, url: str, model: str, prompt: str = False):
        super().__init__(api_key, url, model, prompt)
        self.agents = {}

    def new_agent(self, contract_id):
        contract_id = str(contract_id)
        print(f"{contract_id} - new")
        print(self.agents)
        self.agents[contract_id] = {"start_time": time(), "last_time": time(), "last_doc_time": 0,
                                    "gpt": ChGPT(CHATGPT_KEY, CHATGPT_HOST, CHATGPT_MODEL)}
        print(self.agents)

    def set_promptt(self, contract_id: str, prompt: str):
        contract_id = str(contract_id)
        if contract_id not in self.agents.keys():
            print(contract_id)
            print(self.agents.keys())
            print(self.agents)
            print("contrrrr not in")
            self.new_agent(contract_id)
            callback = "new"
        elif self.agents[contract_id] == 0:
            print("contrrrr ====== 1")
            self.new_agent(contract_id)
            callback = "new"

        self.agents[contract_id].set_prompt(prompt)

    def clear_context(self, contract_id):
        contract_id = str(contract_id)
        self.agents[contract_id] = {"start_time": time(), "last_time": time(), "last_doc_time": 0,
                                    "gpt": ChGPT(CHATGPT_KEY, CHATGPT_HOST, CHATGPT_MODEL)}

    def doc(self, contract_id):
        contract_id = str(contract_id)
        self.agents[contract_id]["last_doc_time"] = time()

    def is_dop_dop(self, contract_id):
        contract_id = str(contract_id)
        if contract_id not in self.agents.keys():
            return False
        if time() - self.agents[contract_id]["last_doc_time"] < MAX_DOCTOR_TIME:
            return True
        return False

    def set_model_l(self, contract_id, model: str):
        contract_id = str(contract_id)
        if contract_id not in self.agents.keys():
            self.new_agent(contract_id)
            callback = "new"
        self.agents[contract_id]["gpt"].set_model(model)
        return True

    def ask(self, contract_id, question):
        callback = "cont"
        print(contract_id)
        contract_id = str(contract_id)
        if contract_id not in self.agents.keys():
            print(contract_id)
            print(self.agents.keys())
            print(self.agents)
            print("contrrrr not in")
            self.new_agent(contract_id)
            callback = "new"
        elif self.agents[contract_id] == 0:
            print("contrrrr ====== 1")
            self.new_agent(contract_id)
            callback = "new"
        elif time() - self.agents[contract_id]["last_time"] > MAX_SESSION_TIME:
            print("Susent")
            self.new_agent(contract_id)
            callback = "new"
        elif time() - self.agents[contract_id]["last_doc_time"] < MAX_DOCTOR_TIME:
            print("Durka")
            return {}, "dop"
        print("aggents", self.agents)
        res = self.agents[contract_id]["gpt"].ask_model(question)
        self.agents[contract_id]["last_time"] = time()

        return res, callback


if __name__ == "__main__":
    gpt = ManyCGPT(CHATGPT_KEY, CHATGPT_HOST, CHATGPT_MODEL)
    print(gpt.ask("1111", "ЭЭЭ у меня башка балит"))
    print(gpt.ask("1111", "А что мне тогида делать?"))
