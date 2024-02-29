# Traefik
## Install CRDs
```
kubectl apply -k "github.com/kubernetes-sigs/gateway-api/config/crd?ref=v0.4.0"
```

## Install Traefik
```
helm repo add traefik https://helm.traefik.io/traefik
helm repo update
helm install traefik traefik/traefik -f values.yaml --version 22.1.0
```

* Expose Traefik dashboard
```
kubectl port-forward $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name) 9000:9000 --address 0.0.0.0
```