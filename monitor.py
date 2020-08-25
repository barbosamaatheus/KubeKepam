PROMETHEUS_URL = 'http://10.66.66.53:32249/api/v1/query?query='

METRICAS = {
    'Traffic':
        'sum(increase(istio_requests_total{destination_workload_namespace="default"}[1m])) by (destination_workload)',
    'LoadTime':
        'sum(irate(istio_request_duration_milliseconds_bucket{reporter="destination", '
        'destination_workload_namespace=~"default"}[1m])) by (destination_workload)'}


def coletar_metrica_prometheus(metrica, range):
    request_prometheus_api = criar_requisicao_prometheus(metrica, range)
    dados = requisitar_prometheus(request_prometheus_api)
    dados_processados = processar_dados(dados)

    return dados_processados


def criar_requisicao_prometheus(metrica, intervalo_tempo):
    return PROMETHEUS_URL + METRICAS.get(metrica) + intervalo_tempo


def requisitar_prometheus(request_prometheus_api):
    from json import loads
    from requests import get

    dados = loads(get(request_prometheus_api).text)
    if dados['data']['result'][0].get('values') is not None:
        dict_requests = {}
        for index in dados['data']['result']:
            try:
                dict_requests[index['metric']['destination_workload']] = index['values']
            except KeyError:
                dict_requests[index['metric']['workload']] = index['values']

        return dict_requests
    else:
        dict_requests = {}
        for index in dados['data']['result']:
            try:
                dict_requests[index['metric']['destination_workload']] = index['value']
            except KeyError:
                dict_requests[index['metric']['workload']] = index['value']

        return dict_requests


def processar_dados(dados):
    from numpy import array
    for key, value in dados.items():
        if array(value).ndim == 1:
            dados[key] = float(value[1])
        else:
            aux_list = []
            for index in value:
                aux_list.append(float(index[1]))
            dados[key] = aux_list
    return dados


def coletar_numero_replicas(namespace):
    dict_namespace = coletar_deployments_from_kubernetes_namespace(namespace)

    for key, value in dict_namespace.items():
        dict_namespace[key] = coletar_replicas_kubernetes(key, 'default')

    return dict_namespace


def coletar_replicas_kubernetes(nome_deployment, namespace):
    from kubernetes.client.rest import ApiException
    from kubernetes import config, client

    configuration = config.load_kube_config()

    # create an instance of the API class
    api_instance = client.AppsV1Api(client.ApiClient(configuration))
    name = nome_deployment  # str | name of the Deployment
    namespace = namespace  # str | object name and auth scope, such as for teams and projects

    try:
        api_response = api_instance.read_namespaced_deployment_scale(name, namespace)
        return api_response.spec.replicas

    except ApiException as e:
        print("Exception when calling AppsV1Api->read_namespaced_deployment_scale: %s\n" % e)


def coletar_deployments_from_kubernetes_namespace(namespace):
    from kubernetes.client.rest import ApiException
    from kubernetes import config, client

    configuration = config.load_kube_config()

    # create an instance of the API class
    api_instance = client.AppsV1Api(client.ApiClient(configuration))

    try:
        api_response = api_instance.list_namespaced_deployment(namespace=namespace)
        dict_namespace = {}
        for i in range(0, len(api_response.items)):
            dict_namespace[api_response.items[i].metadata.name] = 0
        return dict_namespace
    except ApiException as e:
        print("Exception when calling AppsV1beta1Api->list_namespaced_deployment: %s\n" % e)
