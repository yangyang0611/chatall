# Simple Server
>Server for Traefik API Gateway testing, writen in FastAPI

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

### Run on kubernetes
>Use kustomize to render YAML
```
kustomize build ../manifests/base/ | kubectl apply -f -
```

* To curl api
```
curl http://<IP>:<traefik-service-port>/api/v1/status
```

## Build
```
sudo docker build -t simple-server .
```
