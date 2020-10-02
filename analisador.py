def analisar_metricas(data: dict) -> dict:
    """Analisar o valor corrente das métricas nos deployments
       Args:
           data (dict): Dicionário contendo todas as métricas coletadas
           pelo monitor.

       Returns:
           data (dict): Dicionário contendo a proporção entre a métrica
           analisada e o desejado pelo servidor
   """
    cpu_max = 0.8
    load_time_max = 300
    for key in data[list(data.keys())[0]].keys():
        data['CPU'][key] = data['CPU'][key] / cpu_max
        data['LoadTime'][key] = data['LoadTime'][key] / load_time_max
        data['Traffic'][key] = data['Traffic'][key]

    return data


def analisar_metricas_medias(data: dict) -> dict:
    """Analisar o valor médio da métricas presentes nos deployments
       Args:
           data (dict): Dicionário contendo todas as amostras das métricas
            coletadas pelo monitor.

       Returns:
           data (dict): Dicionário contendo a proporção entre a métrica
           analisada e o valor desejado pelo servidor.
   """
    from numpy import array

    cpu_max = 0.8
    load_time_max = 300
    for key in data[list(data.keys())[0]].keys():
        data['CPU'][key] = array(data['CPU'][key]).mean() / cpu_max
        data['LoadTime'][key] = array(data['LoadTime'][key]).mean() / load_time_max
        data['Traffic'][key] = data['Traffic'][key][-1] - data['Traffic'][key][0]

    return data
