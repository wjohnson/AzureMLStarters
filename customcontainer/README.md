Main Article: https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-custom-container
Yaml Schema: https://docs.microsoft.com/en-us/azure/machine-learning/reference-yaml-deployment-managed-online

az account set --subscription 97a44625-84c2-4cba-a587-7d1e95f79a80
az configure --defaults workspace=wjaml group=ml

Get-Content .\Dockerfile | docker build - -t amlcustomcontainer/extendo:v4

docker run --rm -d -p 8080:8080 --name="custom-test" amlcustomcontainer/extendo:v4

docker tag amlcustomcontainer/extendo:v4 ff63410bf6164565b91ccd1199361489.azurecr.io/custom/fastapi:v4
docker push ff63410bf6164565b91ccd1199361489.azurecr.io/custom/fastapi:v4

az configure --defaults workspace=wjaml group=ml
# az ml online-endpoint update -f custom-endpoint.yml
io/custom/fastapi:$(tag)  


DEPLOYMENT_EXISTS=$(az ml online-deployment list --endpoint-name mycustom-endpoint | jq -r '.[].name' | grep "^custom-deployment-yellow$")
if [ -z ${DEPLOYMENT_EXISTS} ]; 
then
    az ml online-deployment update -f custom-deployment.yml --name devops-deploy --set environment.image=ff63410bf6164565b91ccd1199361489.azurecr.io/custom/fastapi:$(tag)
else
    az ml online-deployment create -f custom-deployment.yml --name devops-deploy --set environment.image=ff63410bf6164565b91ccd1199361489.azurecr.io/custom/fastapi:$(tag)
fi

az ml online-endpoint update --name mycustom-endpoint --mirror-traffic "devops-deploy=10"

sleep 10