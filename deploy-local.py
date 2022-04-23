from azureml.core.webservice import LocalWebservice
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment
from azureml.core import Workspace
from azureml.core.model import Model

ws = Workspace.from_config()
model = Model(ws, 'my-sklearn-model')


env = Environment.from_conda_specification(
    name='sklearn-env',
    file_path='./sklearnmodel/sklearn-env.yml'
)

inference_config = InferenceConfig(
    entry_script='sklearnscore.py', environment=env, 
    source_directory="./sklearnmodel/scoring"
)

deployment_config = LocalWebservice.deploy_configuration(port=6789)

local_service = Model.deploy(workspace=ws, 
                       name='sklearn-mnist-local', 
                       models=[model], 
                       inference_config=inference_config, 
                       deployment_config = deployment_config)

local_service.wait_for_deployment(show_output=True)
print(f"Scoring URI is : {local_service.scoring_uri}")