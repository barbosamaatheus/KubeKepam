from monitor import coletar_dados_prometheus, coletar_numero_replicas

load_time = coletar_dados_prometheus('LoadTime', '[5m:1m]')
traffic = coletar_dados_prometheus('Traffic', '[5m:1m]')
pods = coletar_numero_replicas('default')

print('Métrica LoadTime')
for key, value in load_time.items():
    print(key, value)
print()

print('Métrica Traffic')
for key, value in traffic.items():
    print(key, value)
print()

print('Número de pods')
for key, value in pods.items():
    print(key, value)
print()
