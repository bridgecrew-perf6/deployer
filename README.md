# QuestDB deployer

## Installing

1. Install minikube
2. Install VirtualBox to connect to services inside minikube
3. Install python dependencies: `pipenv install`

## Running

1. Run minikube with enough resources minikube: `minikube start --cpus 4 --memory 2000 --driver virtualbox`
2. Expose minikube ports to control `kubectl proxy --port 8080` (to be available on default host `localhost:8080`)
3. Start the app: `python main.py`

## Running tests

Run `pytest`

## Using

### Creating cluster

Run `curl -XPOST localhost:8000`

QuestDB becomes available at minikube ips on NodePort port

1. NodePort is available in the response JSON
2. IP can be checked with `minikube ip`

### Getting cluster info

Run `curl localhost:8000/{cluster-uuid}`

### Deleting cluster

Run `curl -XDELETE localhost:8000/{cluster-uuid}`
