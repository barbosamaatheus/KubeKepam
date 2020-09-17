def tempo_atual():
    """Colete o tempo atual

       Returns:
           O horário atual no formato timestamp
   """
    import time
    return time.time()


def desbloquear_deployment(data, key):
    """Tentativa de desbloqueio de um Deployment impedido de adaptar
       Args:
            data (dict): Dicionário contendo todas as informações
            da adaptação
            key (str): Chave usada para acessar o deployment correto

       Returns:
           data (dict). O dicionário contendo informações atualizadas sobre
           o processo de adaptação.
   """
    if (tempo_atual() - data['TimeAdaptation'][key]) >= 600:  # Faz mais de 10 minutos que ele adaptou?
        data['TimeAdaptation'][key] = 0  # Permita a adaptação
        data['AdaptationStatus'][key] = 0  # Permita a adaptação

    return data


def atualizar_status_deployment(data, key):
    """Atualizar o status adaptativo do Deployment
       Args:
            data (dict): Dicionário contendo todas as informações
            da adaptação
            key (str): Chave usada para acessar o deployment correto

       Returns:
           data (dict). O dicionário contendo informações atualizadas sobre
           o processo de adaptação.
   """
    if data['AdaptationStatus'][key] == 1:  # O deployment está bloqueado para adaptação?
        data = desbloquear_deployment(data, key)  # Tente desbloquear

    if data['AdaptationStatus'][key] == 0:  # Está disponível para adaptar?
        if data['LoadTime'][key] != 0:  # Tem adaptação para agora?
            print('Planejador Adaptando')
            print(key, data['LoadTime'][key])
            data['AdaptationStatus'][key] = 1
            data['TimeAdaptation'][key] = tempo_atual()
    else:  # O deployment está bloqueado
        data['LoadTime'][key] = 0
        print('Planejador Bloqueado')
        print(key, data['LoadTime'][key])

    return data


def calcule_mudanca_trafego(dif_trafego, cpu, number_pods):
    """Planejar ações para adaptar o Cluster
       Args:
            dif_trafego (float): Diferença no tráfego do deployment
            cpu (float): Consumo de CPU do deployment
            number_pods (float): Número de pods implantados neste deployment

       Returns:
           Um inteiro contendo a quantidade de pods necessários
           para lidar com a demanda desejada do servidor.

   """
    if dif_trafego >= 1000 and cpu >= 0.88:
        return calculate_pods(cpu, number_pods)
    elif dif_trafego <= -1000 and cpu <= 0.72:
        return calculate_pods(cpu, number_pods)
    else:
        return 0


def calculate_pods(proporcao, number_pods):
    """Calcular o número de pods dada uma determina proporção
       Args:
            proporcao (float): Diferença entre o valor desejado da métrica
            e o valor corrente
            number_pods (float): Número de pods implantados neste deployment

       Returns:
           Um inteiro contendo a quantidade de pods necessários
           para lidar com a demanda desejada do servidor.
   """
    from math import ceil
    if proporcao > 0.9 or proporcao < 1.1:
        if ceil(number_pods * proporcao) == number_pods:
            return 0
        else:
            return ceil(number_pods * proporcao)
    else:
        return 0


def planejar_adaptacao(data: dict):
    """Planejar ações para adaptar o Cluster
       Args:
           data (dict): Dicionário contendo todas as proporções das métricas
            coletadas pelo monitor.

       Returns:
           data (dict): Dicionário contendo a quantidade de pods necessários
           para lidar com a demanda desejada do servidor.
   """

    for key in data[list(data.keys())[0]].keys():
        data['Traffic'][key] = calcule_mudanca_trafego(data['Traffic'][key], data['CPU'][key], data['Pods'][key])
        data['CPU'][key] = calculate_pods(data['CPU'][key], data['Pods'][key])
        data['LoadTime'][key] = calculate_pods(data['LoadTime'][key], data['Pods'][key])
        data = atualizar_status_deployment(data, key)

    return data
