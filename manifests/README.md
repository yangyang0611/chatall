# Manifests
>common services on kubernetes
## Database
### Mariadb
>Will create database `FRIENDY` while startup
Use kustomize to render YAML for deploy mariadb on kubernetes cluster.
```
kustomize build mariadb | kubectl apply -f -
```
* Connect to Mariadb
```
# Port forward
kubectl port-forward svc/mariadb 3306:3306 --address 0.0.0.0

# Cliecnt connect
mysql -h <host-ip> -u root -p
```
root default password is `password`

## Traceing solution
>Deploy Jaeger and Traefik in order (in default namespace).
### Jaeger
See jaeger/README.md for more information.

### Traefik
See traefik/README.md for more information.

### Support
https://traefik.io/blog/distributed-tracing-with-traefik-and-jaeger-on-kubernetes/
