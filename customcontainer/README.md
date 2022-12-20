# Creating and Deploying a Custom Container for Azure ML

Main Article: https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-custom-container
Yaml Schema: https://docs.microsoft.com/en-us/azure/machine-learning/reference-yaml-deployment-managed-online

## Running the server locally

Using flask:

```bash
cd ./customcontainer/server
python -m flask run --host=0.0.0.0 -p 3000
```

Using Docker (after it has been built):

```
docker run -d -p 3000:3000 --name="flask-ml-test" flaskml:v1
```

## Steps

Run the following commands to set up your account, build the image, and push it to an azure container registry.

```powershell
$Env:SUBSCRIPTION_ID = "SUBSCRIPTION_ID"
$ENV:ML_WKSP_NAME = "ML_WKSP_NAME"
$ENV:ML_RG_NAME = "ML_RG_NAME"
$ENV:ACR_NAME = "ACR_NAME"
$ENV:TAG_NAME = "v1"
cd ./customcontainer
az account set --subscription $Env:SUBSCRIPTION_ID
az configure --defaults workspace=$Env:ML_WKSP_NAME group=$Env:ML_RG_NAME

docker build --tag "flaskml:$ENV:TAG_NAME" .
docker tag "flaskml:$ENV:TAG_NAME" "$ENV:ACR_NAME.azurecr.io/flaskml:$ENV:TAG_NAME"
# Optionally test it:
# docker run -d -p 3000:3000 --name="flask-ml-test" flaskml:v1

az acr login -n "$ENV:ACR_NAME"
docker push "$ENV:ACR_NAME.azurecr.io/flaskml:$ENV:TAG_NAME"

```

**If the endpoint and deployment do not exist**

```powershell
az ml online-endpoint create --file ./custom-endpoint.yml

az ml online-deployment create `
-f custom-deployment.yml `
--name custom-acr `
--set environment.image="$ENV:ACR_NAME.azurecr.io/flaskml:$ENV:TAG_NAME" `
--skip-script-validation `
```

**If the endpoint and deployment DO exist**

```powershell
az ml online-deployment update `
-f custom-deployment.yml `
--name custom-acr `
--set environment.image="$ENV:ACR_NAME.azurecr.io/flaskml:$ENV:TAG_NAME" `

az ml online-endpoint update `
-f custom-endpoint.yml `
--traffic "custom-acr=100"
```


DEPLOYMENT_EXISTS=$(az ml online-deployment list --endpoint-name mycustom-endpoint | jq -r '.[].name' | grep "^custom-deployment-yellow$")
if [ -z ${DEPLOYMENT_EXISTS} ]; 
then
    az ml online-deployment update -f custom-deployment.yml --name devops-deploy --set environment.image=ff63410bf6164565b91ccd1199361489.azurecr.io/custom/fastapi:$(tag)
else
    az ml online-deployment create -f custom-deployment.yml --name devops-deploy --set environment.image=ff63410bf6164565b91ccd1199361489.azurecr.io/custom/fastapi:$(tag)
fi

az ml online-endpoint update --name mycustom-endpoint --mirror-traffic "devops-deploy=10"

sleep 10