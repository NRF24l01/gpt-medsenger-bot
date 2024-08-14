import json


def get_model(contract_id: int, contrmodels: dict, base_model: str):
    if not contract_id in contrmodels.keys():
        contrmodels[contract_id] = base_model
        with open("contract_model.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(contrmodels, indent=4))
        return contrmodels, base_model
    return contrmodels, contrmodels[contract_id]
