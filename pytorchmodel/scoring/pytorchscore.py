import os
import json

import torch
import numpy as np

from scoring.model import Net


def init():
    global model
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "tensor_dict.pt")
    model = Net()
    model.load_state_dict(torch.load(model_path))

def run(data):
    input_data = json.loads(data)
    np_arr = np.array(input_data)
    input_tensor = torch.from_numpy(np.float32(np_arr))
    return model(input_tensor).detach().numpy().tolist()