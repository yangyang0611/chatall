# Lab 2
## friendy-server
The backend-server to provide main control logic of friendy service.

## friendy-webpage
The frontend-server to render visualize interface and the provide gateway for interconnetion with backend-server.

## video-chat
The realtime multiuser online video-chat application build on redis-server.

## chatcord
The realtime multiuser online text-chat application build with socket.io.

## manifests
keep some kubenretes yaml for deploy application on kubernetes (using kustomize to render yaml).

## simple-server
Simple server writen in FastAPI for Traefik API Gateway testing.

### Run
To run the whole project, you have to run each friend-webpage, video-chat, and chatcord server.
```
cd friendy-webpage
cd video-chat
cd chatcord
```

In each repository, run each server respectively. The steps of running is written in each repository.