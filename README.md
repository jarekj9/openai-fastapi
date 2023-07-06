
# openai with fastapi
##### Build container:
```
docker build -t fastapi-openai:latest .
```
##### Test container locally:
```
docker run --rm -ti --p 8003:80 fastapi-openai
```
##### Deploy to Azure Container Instances:
```
docker tag fastapi-openai registryname.azurecr.io/fastapi-openai:latest
az acr login -n registryname.azurecr.io
docker push  registryname.azurecr.io/fastapi-openai:latest
az container create --resource-group RG-name --file container-deployment.yaml
```
##### Deploy to Azure App Service:
- create app service  ( linux, python 3.10)
- push code to github
- connect github in app service
- in app properties startup command ```python3 app/main.py```

