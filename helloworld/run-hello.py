# get-started/run-hello.py
from azureml.core import Workspace, Experiment, ScriptRunConfig

ws = Workspace.from_config()
experiment = Experiment(workspace=ws, name='experiment-hello')

config = ScriptRunConfig(source_directory='./helloworld/train', script='hello.py', compute_target='cpu-cluster')

run = experiment.submit(config)
aml_url = run.get_portal_url()
print(aml_url)