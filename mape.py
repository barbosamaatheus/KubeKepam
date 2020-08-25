from monitor import coletar_metrica_prometheus, coletar_numero_replicas

load_time = coletar_metrica_prometheus('LoadTime', '[5m:1m]')
traffic = coletar_metrica_prometheus('Traffic', '[5m:1m]')
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


"""
Load Time
Traffic
Numero de conteineres

Recency *
Number of Logins *
Stability *
Number of Logins *
"""
