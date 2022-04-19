# run-pytorch.py
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import Environment
from azureml.core import ScriptRunConfig

if __name__ == "__main__":
    ws = Workspace.from_config()
    experiment = Experiment(workspace=ws, name='experiment-sklearn')
    config = ScriptRunConfig(source_directory='./sklearnmodel/train',
                             script='train.py',
                             compute_target='cpu-cluster')

    # set up custom sklearn environment
    # This will result in an image build
    env = Environment.from_conda_specification(
        name='sklearn-env',
        file_path='./sklearnmodel/sklearn-env.yml'
    )
    # Alternatively, we could use a pre-built model
    # env = Environment.get(ws, name='AzureML-sklearn-1.0-ubuntu20.04-py38-cpu')
    config.run_config.environment = env

    run = experiment.submit(config)

    aml_url = run.get_portal_url()
    print(aml_url)