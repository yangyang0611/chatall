# Friendy Server

## Environments
### Python package
```
pip3 install -r requirements.txt
```

### Traefik
see manifests/traefik for more info

## Usage
### Run on local
* Start up FastAPI server
```
uvicorn main:app --reload --port 8501 --host 0.0.0.0
```

You can visit api doc through: http://<IP>:<Port>/docs

### Run with docker
>Use pre-build container or build your container by yourself
```
sudo docker run -d -p 8501:8501 --name friendy alan0415/friendy-server:v0.1
```

### Run on kubernetes
>Use kustomize to render YAML; use `overlay/dev` to use latest build
```
kustomize build ../manifests/friendy-server/base | kubectl apply -f -
```

* To view api doc
>Check your NodePort
```
curl http://<IP>:<Port>/docs
```

* To curl api
```
curl http://<IP>:<traefik-service-port>/api/v1/<path>
```

## Build
```
sudo docker build -t friendy-server .
```

## Test
>Use pytest
```
# under `2023-nycu-icsdt-g2/lab/lab2/friendy-server`
pytest 
```

## Support
https://fastapi.tiangolo.com/tutorial/bigger-applications/
https://myapollo.com.tw/blog/python-pydantic/
