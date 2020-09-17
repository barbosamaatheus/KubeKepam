def analisar_metricas(data: dict):
    """Analisar o valor corrente das métricas nos deployments
       Args:
           data (dict): Dicionário contendo todas as métricas coletadas
           pelo monitor.

       Returns:
           data (dict): Dicionário contendo a proporção entre a métrica
           análisada e o desejado pelo servidor
   """

    for key in data[list(data.keys())[0]].keys():
        data['CPU'][key] = data['CPU'][key] / 0.8
        data['LoadTime'][key] = data['LoadTime'][key] / 300
        data['Traffic'][key] = data['Traffic'][key]

    return data


def analisar_metricas_medias(data: dict):
    """Analisar o valor médio da métricas presentes nos deployments
       Args:
           data (dict): Dicionário contendo todas as amostras das métricas
            coletadas pelo monitor.

       Returns:
           data (dict): Dicionário contendo a proporção entre a métrica
           análisada e o valor desejado pelo servidor.
   """
    from numpy import array
    for key in data[list(data.keys())[0]].keys():
        data['CPU'][key] = array(data['CPU'][key]).mean() / 0.8
        data['LoadTime'][key] = array(data['LoadTime'][key]).mean() / 300
        data['Traffic'][key] = data['Traffic'][key][-1] - data['Traffic'][key][0]

    return data
