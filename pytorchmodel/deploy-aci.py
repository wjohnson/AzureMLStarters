from azureml.core import Workspace
from azureml.core.model import Model

from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig
from azureml.core import Environment

if __name__ == "__main__":
    ws = Workspace.from_config()

    model = ws.models.get("my-pytorch-model")
    # set up pytorch environment
    env = Environment.from_conda_specification(
        name='pytorch-env',
        file_path='./pytorchmodel/pytorch-env.yml'
    )

    inference_config = InferenceConfig(
        entry_script='pytorchscore.py', environment=env, 
        source_directory="./pytorchmodel/scoring"
    )
    deployment_config = AciWebservice.deploy_configuration(
        cpu_cores = 1, memory_gb = 1)
    service = Model.deploy(ws, "myptorchservice", [model], 
        inference_config, deployment_config)
    service.wait_for_deployment(show_output = True)
    print(service.state)