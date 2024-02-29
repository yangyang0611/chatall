# Jaeger
## Deploy
* Install cert-manager (pre-requirement)
```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.6.3/cert-manager.yaml
```

* Install Operator
```
# update helm repo
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update
# create ns
kubectl create ns observability
helm install my-jaeger-operator jaegertracing/jaeger-operator --version 2.25.0 -n observability
```

* Install jaeger
```
kubectl apply -f jaeger.yaml
```

* Expose dashboard
```
kubectl port-forward svc/jaeger-query 16686:16686 --address 0.0.0.0
```