from monitor import coletar_dados_prometheus, criar_base_quarentena
from analisador import analisar_metricas_medias
from planejador import planejar_adaptacao
from executor import executar_adaptacao
from time import sleep

data = {}
first = True

while True:
    # Monitoramento
    data['LoadTime'] = coletar_dados_prometheus('LoadTime', '[5m:1m]')
    data['Traffic'] = coletar_dados_prometheus('Traffic', '[5m:1m]')
    data['CPU'] = coletar_dados_prometheus('CPU', '[5m:1m]')
    data['Pods'] = coletar_dados_prometheus('Pods', '')  # Coleta via Prometheus
    # data['Pods'] = coletar_numero_replicas('default') # Coleta via Kubernetes

    if first:
        data['AdaptationStatus'], data['TimeAdaptation'] = criar_base_quarentena(data)
        first = False

    data = analisar_metricas_medias(data)  # Análise
    data = planejar_adaptacao(data)  # Planejamento
    executar_adaptacao(data)  # Execução

    sleep(15)
