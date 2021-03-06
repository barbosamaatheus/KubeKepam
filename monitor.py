from typing import Tuple, Dict

PROMETHEUS_URL = 'http://10.66.66.53:30782/api/v1/query?query='  # URL do prometheus Istio
PROMETHEUS_KUBE_PROMETHEUS = 'http://10.66.66.53:30298/api/v1/query?query='  # URL do prometheus KubePrometheus

METRICAS = {
    'Traffic':
        'sum(increase(istio_requests_total{destination_workload_namespace="default"}[1m])) by (destination_workload)',
    'LoadTime':
        '(histogram_quantile(0.90, sum(irate(istio_request_duration_milliseconds_bucket{reporter="destination", '
        'destination_workload_namespace=~"default"}[1m])) by (le, destination_workload)))',
    'CPU':
        '(sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_rate{namespace="default"}* on('
        'namespace,pod) group_left(workload, workload_type) namespace_workload_pod:kube_pod_owner:relabel{'
        'namespace="default", workload_type="deployment"}) by (workload)/sum('
        'kube_pod_container_resource_requests_cpu_cores{namespace="default"}* on(namespace,pod) group_left(workload, '
        'workload_type) namespace_workload_pod:kube_pod_owner:relabel{namespace="default", '
        'workload_type="deployment"}) by (workload))',
    'Pods':
        'count(namespace_workload_pod:kube_pod_owner:relabel{namespace="default", workload_type="deployment"}) by ('
        'workload)'}


def coletar_dados_prometheus(metrica: str, intervalo_prometheus: str = '') -> dict:
    """Coletar quaisquer métricas do Prometheus
        Args:
            metrica (str): Chave da métrica do Prometheus a ser consultada
            no dicionário METRICAS.

            intervalo_prometheus (str): intervalo de informações que será retornado.

        Returns:
            dados_processados (dict):

            Se a variável range for vazia, o usuário receberá um
            dicionário com todos os deployments e o seus valores
            no instante atual.

            Por exemplo: {adservice: 100,
                          frontned: 50}

            Se a variável range for especificado, o usuário receberá um
            dicionário com todos os deployments e os valores da métrica
            conforme sua especificação.

            Por exemplo: Se range = ['2m:1m']
                         {adservice: [100, 102],
                          frontend: [50, 100]}

            Por exemplo: Se range = ['4m:1m']
                         {adservice: [100, 102, 109, 112],
                          frontend: [50, 100, 115, 125]}
    """
    requisicao_prometheus_api = criar_requisicao_prometheus(metrica, intervalo_prometheus)
    dados = requisitar_prometheus(requisicao_prometheus_api)
    print(type(dados))
    dados_processados = processar_dados(dados)

    return dados_processados


def criar_requisicao_prometheus(metrica: str, intervalo_prometheus: str) -> str:
    """Constrói a requisição do Prometheus
        Args:
            metrica (str): Chave da métrica do Prometheus a ser consultada
            no dicionário METRICAS.

            intervalo_prometheus (str): intervalo de informações que será retornado.

        Returns:
            A URL de consulta ao Prometheus para uma determinada métrica (str)
    """
    if metrica not in ['CPU', 'Pods']:
        return PROMETHEUS_URL + METRICAS.get(metrica) + intervalo_prometheus
    else:  # URL do Kube Prometheus
        return PROMETHEUS_KUBE_PROMETHEUS + METRICAS.get(metrica) + intervalo_prometheus


def requisitar_prometheus(request_prometheus_api: str) -> dict:
    """Coletar dados no prometheus através de um GET.

        Args:
            request_prometheus_api (str): A URL de consulta ao Prometheus
            para uma determinada métrica.

        Returns:
            Dado bruto do Prometheus seguindo a estruturação do json (dict).
    """
    from json import loads
    from requests import get

    return loads(get(request_prometheus_api).text)


def processar_dados(dados: dict) -> dict:
    """Processar e tratar os dados coletados no Prometheus.
        Args:
            dados (dict): Dados brutos de um determina consulta ao Prometheus.

        Returns:
            Informações processadas e tratadas (dict).

            Se a variável range for vazia, o usuário receberá um
            dicionário com todos os deployments e o seus valores
            no instante atual.

            Por exemplo: {adservice: 100,
                          frontned: 50}

            Se a variável range for especificado, o usuário receberá um
            dicionário com todos os deployments e os valores da métrica
            conforme sua especificação.

            Por exemplo: Se range = ['2m:1m']
                         {adservice: [100, 102],
                          frontend: [50, 100]}

            Por exemplo: Se range = ['4m:1m']
                         {adservice: [100, 102, 109, 112],
                          frontend: [50, 100, 115, 125]}
    """
    from numpy import array

    # Caso o usuário tenha informado algum range (Processar N respostas).
    if dados['data']['result'][0].get('values') is not None:
        dict_requests = {}
        for index in dados['data']['result']:
            try:
                dict_requests[index['metric']['destination_workload']] = index['values']
            except KeyError:
                dict_requests[index['metric']['workload']] = index['values']
    # Caso o usuário não tenha informado nenhum range (Processar 1 resposta).
    else:
        dict_requests = {}
        for index in dados['data']['result']:
            try:
                dict_requests[index['metric']['destination_workload']] = index['value']
            except KeyError:
                dict_requests[index['metric']['workload']] = index['value']

    # Removendo dados inúteis do dicionário, p. e.x., tempo da métrica.
    dados_processados = {}
    for key, value in dict_requests.items():
        if array(value).ndim == 1:
            dados_processados[key] = float(value[1])
        else:
            aux_list = []
            for index in value:
                aux_list.append(float(index[1]))
            dados_processados[key] = aux_list
    return dados_processados


def coletar_numero_replicas(namespace: str):
    """API do Kubernetes responsável por coletar o número de réplicas
        de um Deployment implantando no Kubernetes.

        Args:
            namespace (str): Namespace da aplicação no Kubernetes

        Returns:
            Dicionário com a quantidade de pods por deployment (dict).

            Por exemplo: {adservice: 1,
                          frontned: 2}
    """
    from kubernetes.client.rest import ApiException
    from kubernetes import config, client

    configuration = config.load_kube_config()
    api_instance = client.AppsV1Api(client.ApiClient(configuration))

    try:
        api_response = api_instance.list_namespaced_deployment(namespace=namespace)
        dict_namespace = {}
        for i in range(0, len(api_response.items)):
            deployment = api_response.items[i].metadata.name
            dict_namespace[deployment] = api_instance.read_namespaced_deployment_scale(deployment,
                                                                                       namespace).spec.replicas
        return dict_namespace
    except ApiException as e:
        print("Exception when calling AppsV1beta1Api->list_namespaced_deployment: %s\n" % e)


def criar_base_quarentena(dados: dict) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Criar a estrutura para lidar com função de contenção
        de adaptações sucessivas no KubeKepam

        Args:
            dados (dict): nome do namespace do Kubernetes.

        Returns:
            Dicionário com a estrutura da função adaptação
             sucessivas KubeKepam.

            Por exemplo:
            'AdaptationStatus': {'currencyservice': 0, 'emailservice': 0}
            'TimeAdaptation': {'currencyservice': 0, 'emailservice': 0}
    """
    adaptation_status = {}
    time_after_adaptation = {}

    for key in dados[list(dados.keys())[0]].keys():
        adaptation_status[key] = 0
        time_after_adaptation[key] = 0

    return adaptation_status, time_after_adaptation
