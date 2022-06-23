from kubernetes_asyncio import client, config
from kubernetes_asyncio.client.api_client import ApiClient
from config.k8s import K8S_HOST


def get_core_client():
    configuration = client.Configuration()
    configuration.host = K8S_HOST

    api_client = ApiClient(configuration)
    return client.CoreV1Api(api_client)


def get_apps_client():
    configuration = client.Configuration()
    configuration.host = K8S_HOST

    api_client = ApiClient(configuration)
    return client.AppsV1Api(api_client)
