# Simplified Azure ML Starters

These starters are designed to help you understand what options are available and allow you to quickly edit the scripts for faster deployments of your own.

Examples and resource links covered:

* [Hyperparameter Sweeps](#hyperparmeter-sweeps)
* [Parallel Training on Many Files](#parallel-training-on-many-files)
* [Custom Containers](#custom-containers)
* [Distributed Training](#distributed-training)

Certain data sources are important to connect to but require using other python packages with no built-in connector.

* [Connect to Snowflake](#connect-to-snowflake)
* [Connect to Azure Synapse](#connect-to-azure-synapse)

## Hyperparmeter Sweeps

Hyperparameter sweeps take a training script and command 

* Use Hyperparameter Sweeps in a [pipeline](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-sweep-in-pipeline)
* Use Hyperparameters Sweeps in a [job](https://learn.microsoft.com/en-us/azure/machine-learning/reference-yaml-job-sweep)

Follow these steps to launch the sample:

* Upload the [bank marketing](#bank-marketing) dataset below.
* Execute this CLI command
  ```bash
  az ml job create --file ./hyperparameter/job-hyperparam-opt.yml
  ```


## Parallel Training on Many Files

You can use a parallel task on an Azure ML pipeline to train on micro batches of a large file or across many individual files.

* [Parallel Job Overview Microsoft Docs](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-parallel-job-in-pipeline?tabs=cliv2)
* [CLI V2 Yaml Schema for Parallel Tasks](https://learn.microsoft.com/en-us/azure/machine-learning/reference-yaml-job-parallel)

* Set up the [Online Retail 2 dataset](#online-retail-2)
* Execute the command below:
  ```bash
  az ml job create --file ./parallel-pipeline/main.yaml
  ```

  ## Registered Components

  You can register components and re-use them.

  * [Registered Components Microsoft Docs](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-component-pipelines-ui)

  * Set up the [Online Retail 2 dataset](#online-retail-2)
  * Execute the command below to register a couple components you might re-use
    ```bash
    az ml component create --file ./registered-components/component-lag/lagger.yml
    az ml component create --file ./registered-components/component-dense-dates/densedate.yml
    ```
    * If you are running these commands multiple times you may need to add the `--version` flag.
  * Execute the command below to run the pipeline using local and registered components
    ```bash
    az ml job create --file ./registered-components/main.yml
    ```

## Custom Containers

* [Deploy a Custom Container on Azure ML](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-custom-container)
  * The container needs to have the following:
  * A web server that has a liveness, readiness, and scoring route.
  * It must reference some model object since model is required (this example uploads a random serialized python function)
* Getting Started with [Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli?tabs=azure-cli)

### Building a Docker Container and Deploying to an Online Endpoint

```powershell
if (-Not (Test-Path -PathType Container .\customcontainer\pyobject)){
    New-Item -ItemType Directory -Force -Path .\customcontainer\pyobject
}
python -c "import joblib;joblib.dump(123, './customcontainer/pyobject/model.joblib');" 
Get-Content .\Dockerfile | docker build - -t USERNAME/IMAGENAME:v1
# Confirm it's working locally
docker run --rm -d -p 8080:8080 --name="custom-test" USERNAME/IMAGENAME:v1

# Tag the local docker image to include your azurecr.io domain
docker tag USERNAME/IMAGENAME:v1 YOURACRNAME.azurecr.io/USERNAME/IMAGENAME:v1
# Login to Azure and your registry
az login
az acr login --name YOURACRNAME
# Push the 
docker push YOURACRNAME.azurecr.io/USERNAME/IMAGENAME:v1
```

Next run this command using the azure CLI

```bash
DEPLOYMENT_EXISTS=$(az ml online-deployment list --endpoint-name mycustom-endpoint | jq -r '.[].name' | grep "^custom-deployment$")
if [ -z ${DEPLOYMENT_EXISTS} ]; 
then
    az ml online-deployment update -f custom-deployment.yml --name devops-deploy --set environment.image=YOURACRNAME.azurecr.io/USERNAME/IMAGENAME:v1 --all-traffic
else
    az ml online-deployment create -f custom-deployment.yml --name devops-deploy --set environment.image=YOURACRNAME.azurecr.io/USERNAME/IMAGENAME:v1
    az ml online-endpoint update --name mycustom-endpoint --traffic "devops-deploy=100"
fi

sleep 10
```

## Distributed Training

In the command task, you define the distribution.

* Sample using [Tensorflow and the MPI Distribution](https://github.com/Azure/azureml-examples/blob/83c67ec408f10e2e07b3a2a3e648023caa09e112/sdk/python/jobs/single-step/tensorflow/mnist-distributed-horovod/tensorflow-mnist-distributed-horovod.ipynb)


## Data Sources:

The datasets are [registered via the CLI (official docs)](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-data-assets?tabs=cli).

You should configure your defaults for the Azure CLI.

```bash
az account set --subscription <subscription>
az configure --defaults workspace=<workspace> group=<resource-group> location=<location>
```

### Bank Marketing 

* [(Bank Marketing @ UCI)](https://archive.ics.uci.edu/ml/datasets/Bank+Marketing)
  * Used in Hyperparameter Sweep


```powershell
if (-Not (Test-Path -PathType Container .\downloads)){
    New-Item -ItemType Directory -Force -Path .\downloads
}
$source = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip'
$destination = '.\downloads\bank.zip'
Invoke-RestMethod -Uri $source -OutFile $destination
Expand-Archive .\downloads\bank.zip -DestinationPath .\datasets\bank
az ml data create -f ./datasets/bank-marketing.yml

```

### Online Retail 2

* [Online Retail 2]()
  * Used in parallel-pipeline
  * Used in registered-components

```powershell
if (-Not (Test-Path -PathType Container .\datasets)){
    New-Item -ItemType Directory -Force -Path .\datasets
}
if (-Not (Test-Path -PathType Container .\datasets\retail)){
    New-Item -ItemType Directory -Force -Path .\datasets\retail
}
$source = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx'
$destination = '.\datasets\retail\online_retail_II.xlsx'
Invoke-RestMethod -Uri $source -OutFile $destination
az ml data create -f ./datasets/online-retail-ii.yml

```

### Connect to Snowflake

* Leverage the work of [Mash Syed (mashhype)](https://github.com/mashhype/) with an [example that uses snowpark](https://github.com/mashhype/azureml-snowflake-snowpark-code/blob/main/azureml/azureml-snowflake-snowpark-sample.ipynb)
* It relies on the [Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html)

### Connect to Azure Synapse

There is no native connector to Azure Synapse so you'll need to use Pyodbc / SQLAlchemy.

```python
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

server = 'yoursqlpoolname.sql.azuresynapse.net'
database = 'yourdatabase'
username = 'sqlusername'
password = 'XXX' # You might store this in a key vault and use the Key Vault Client library to get the secrets

# Querying a table with sqlalchemy
connection_url = sqlalchemy.engine.URL.create(
    "mssql+pyodbc",
    username=username,
    password=password,
    host=server,
    database=database,
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "autocommit": "True",
    },
)

engine = create_engine(connection_url).execution_options(
    isolation_level="AUTOCOMMIT"
)

with engine.connect() as conn:
    df = pd.read_sql_table("table_name", conn)
    print(df.shape)


```