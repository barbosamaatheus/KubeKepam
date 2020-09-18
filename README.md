# KubeKepam

O *Kube Kepam* é uma solução auto adaptativa que gerencia quaisquer Microservice-Based Applications (MBAs) implantadas em Cluster Kubernetes. 
O seu objetivo é garantir que quaisquer requisitos específicados pelo desenvolvedores não sejam violados em tempo de execução. Ele é um projeto da disciplina Desenvolvimento de Aplicações com Arquitetura Baseada em Microsserviços. 
Essa disciplina é ofertada em conjunto para a graduação [(IF1007)](https://github.com/IF1007/if1007) e pós graduação [(IN1108)](https://github.com/IF1007/if1007) no Centro de Informática da Universidade Federal de Pernambuco (UFPE).


## Tabela de Conteúdo

- [KubeKepam](#kubekepam)
  - [Tabela de Conteúdo](#tabela-de-conteúdo)
  - [Equipe](#equipe)
  - [Justificativa](#justificativa)
  - [Arquitetura Conceitual](#arquitetura-conceitual)
  - [Arquitetural Implementável](#arquitetural-implementável)
  - [Link das Tecnologias](#link-das-tecnologias)
  - [Guia de Instalações e Scipts](#guias-com-instalações-e-scipts-automatizados)


## Equipe

| [Matheus Oliveira](https://github.com/barbosamaatheus) (mbo2) |  [Nailson Barros](https://github.com/Nailsonnb) (nnb) | [Wellison Santos](https://github.com/wellisonraul) (wrms) |
| ------ | ------ | ------ |
| Desenvolvedor | Desenvolvedor | Desenvolvedor |


## Justificativa

O monitoramento automático com o mínimo de intervenção humana de quaisquer aplicações implantadas na nuvem ainda não está estabelecida na indústria. 
No geral, boa parte das soluções proposta na literatura e na industria focam em métricas comuns da computação como memória, cpu e rede.
Porém, poucos trabalhos focam em métricas como tempo de resposta, latência, número de requisições. 
O *Kube Kepam* surge como uma alternativa ao propor mecanismos adaptativos que consideram tais métricas 

## Arquitetura Conceitual

**O que é o MAPE-K?**

O MAPE-K consiste em um modelo de computação autônoma desenvolvido pela IBM. Esse modelo é composto pelas fases de monitoramento, análise, planejamento e execução em conjunto com uma base de conhecimento. Um modelo genérico MAPE-K é apresentado a seguir: 

<p align="center">
<img src="https://gitcin.cin.ufpe.br/wrms/kubekepam/raw/master/docs/img/the_mape-k-control-loop.png" />
</p>


**Como funciona o MAPE-K do KubeKepam?**

O KubeKepam é uma aplicação composta pelos 4 principais compontes do MAPE-K, sendo eles: monitor, analisador, planejador e executor. A Figura abaixo apresenta o KubeKepam.

<p align="center">
<img width="489" height="383" src="https://gitcin.cin.ufpe.br/wrms/kubekepam/raw/master/docs/img/kube_kepam_teorica_resumo.png" />
</p>

* **Monitor:** Este componente coleta em tempo de execução métricas de desempenho e de negócio dos microsserviços. As métricas são coletadas através de API's disponíveis em bancos de dados como o Prometheus ou  InfluxDB. Neste tipo de banco, é possível coletar o último valor da métrica ou agregado passado de valores. 
* **Analisador:** Este componente avalia as métricas coletadas pelo *Monitor* e determina se existem possíveis "sintomas" de uma possível queda no comportamento habitual da aplicação. No geral, existem diversas alternativas para analisar o comportamento do elemento monitorado variando conforme o contexto da aplicação. Nesta solução, é examinada a proporção no uso de recursos da aplicação, assim como feita pelo [HPA Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
* **Planejador:** Este componente avalia os "sintomas" observados pelo *Analisador* e planeja ações que possam redirecionar a aplicação ao seu estado habitual de comportamento. Assim como na análise, diversas alternativas são viáveis para propor ações que tentarão "remover os sintomas presentes". Neste projeto, o *Planejador* calcula  a quantidade de pods necessárias para reajustar o uso dos recursos, assim como feita pelo [HPA Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
* **Executor:** Este componente conhece a quantidade de pods necessárias para cada microsserviço da aplicação disponibilizadas pelo *Planejador*. Sua função, portanto, é apenas atualizar a quantidade de pods por microsserviços através de requisições no Cluster Kubernetes. 


## Arquitetural Implementável

## Link das Tecnologias

* [Online Boutique](docs/OnlineBoutique.md)
* [Kube-Prometheus](https://github.com/prometheus-operator/kube-prometheus)
* [Istio](docs/ISTIO.md)
* [Kubernetes](docs/Kubernetes.md)
* [API Python do Kubernetes](https://github.com/kubernetes-client/python)
* [Python](python.org)

## Guias com instalações e Scipts Automatizados