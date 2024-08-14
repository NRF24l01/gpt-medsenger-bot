import json


def get_model(contract_id: int, contrmodels: dict, base_model: str):
    if not contract_id in contrmodels.keys():
        contrmodels[contract_id] = base_model
        with open("contract_model.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(contrmodels))
        return contrmodels, base_model
    return contrmodels, contrmodels[contract_id]


def get_prompt(contract_id: int, contrmodels: dict, base_pr: str):
    if not contract_id in contrmodels.keys():
        contrmodels[contract_id] = base_pr
        with open("contract_prompts.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(contrmodels))
        return contrmodels, base_pr
    return contrmodels, contrmodels[contract_id]
