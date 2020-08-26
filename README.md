# KubeKepam

Projeto da disciplina Desenvolvimento de Aplicações com Arquitetura Baseada em Microsserviços. 
Essa disciplina é ofertada em conjunto para a graduação [(IF1007)](https://github.com/IF1007/if1007) e pós graduação [(IN1108)](https://github.com/IF1007/if1007) no Centro de Informática da Universidade Federal de Pernambuco (UFPE).

## Equipe

| [Matheus Oliveira](https://github.com/barbosamaatheus) (mbo2) |  [Nailson Barros](https://github.com/Nailsonnb) (nnb) | [Wellison Santos](https://github.com/wellisonraul) (wrms) |
| ------ | ------ | ------ |
| Desenvolvedor | Desenvolvedor | Desenvolvedor |

## Descrição
O *Kube Kepam* é uma solução auto adaptativa que gerencia quaisquer Microservice-Based Applications (MBAs) implantadas em Cluster Kubernetes. 
O seu objetivo é garantir que quaisquer requisitos específicados pelo desenvolvedores não sejam violados em tempo de execução. Basicamente, a aplicação realiza:

* Monitora dos recursos da aplicação, p. ex.: memória, cpu e tempo de resposta;
* Analisa os recursos monitorados para identificar possíveis desvios a requisitos pré-estabelecidos;
* Planeja ações que são capazes de levar as MBAs de um estado A (defeituoso) para um estado B (normal);
* Executa ações que modificam a estrutura da aplicação, p. ex.: aumento do número de réplicas.

## Justificativa

O monitoramento automático com o mínimo de intervenção humana de quaisquer aplicações implantadas na nuvem ainda não está estabelecida na indústria. 
No geral, boa parte das soluções proposta na literatura e na industria focam em métricas comuns da computação como memória, cpu e rede.
Porém, poucos trabalhos focam em métricas como tempo de resposta, latência, número de requisições. 
O *Kube Kepam* surge como uma alternativa ao propor mecanismos adaptativos que consideram tais métricas 

## Tecnologias

* [Online Boutique](docs/OnlineBoutique.md)
* [Kube-Prometheus](https://github.com/prometheus-operator/kube-prometheus)
* [Istio](docs/ISTIO.md)
* [Kubernetes](docs/Kubernetes.md)
* [API Python do Kubernetes](https://github.com/kubernetes-client/python)
* [Python](python.org)