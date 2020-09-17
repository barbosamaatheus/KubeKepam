def executar_adaptacao(data):
    """Executar a adaptação planejada
       Args:
            data (dict): Dicionário contendo todas as informações
            da adaptação
   """

    for key in data[list(data.keys())[0]].keys():
        if data['LoadTime'][key] != 0:
            scale_deployment(key, 'default', data['LoadTime'][key])


def scale_deployment(nome_deployment, namespace, replicas):
    """Scale o deployment Kubernetes
       Args:
            nome_deployment (str): Refere-se ao deployment implantado no Kubernetes
            namespace (str): Namespace em que o deployment está inserido
            replicas (int): Número de réplicas que será associado a este deployment
   """
    from kubernetes.client.rest import ApiException
    from kubernetes import config, client

    configuration = config.load_kube_config()

    api_instance = client.AppsV1Api(client.ApiClient(configuration))
    name = nome_deployment  # str | name of the Scale
    namespace = namespace  # str | object name and auth scope, such as for teams and projects
    body = {'spec': {'replicas': replicas}}  # UNKNOWN_BASE_TYPE |
    pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)

    try:
        api_response = api_instance.patch_namespaced_deployment_scale(name, namespace, body, pretty=pretty)
    except ApiException as e:
        print("Exception when calling AppsV1Api->patch_namespaced_deployment_scale: %s\n" % e)
