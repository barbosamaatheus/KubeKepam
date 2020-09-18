# ![Logo](/docs/img/logo.png) KubeKepam

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

##### O que é o MAPE-K?

O MAPE-K consiste em um modelo de computação autônoma desenvolvido pela IBM. Esse modelo é composto pelas fases de monitoramento, análise, planejamento e execução em conjunto com uma base de conhecimento. Um modelo genérico MAPE-K é apresentado a seguir: 

<p align="center">
<img src="https://gitcin.cin.ufpe.br/wrms/kubekepam/raw/master/docs/img/the_mape-k-control-loop.png" />
</p>


##### Como funciona o MAPE-K do KubeKepam?

O KubeKepam é uma aplicação composta pelos 4 principais compontes do MAPE-K, sendo eles: monitor, analisador, planejador e executor. A Figura abaixo apresenta o KubeKepam.

<p align="center">
<img width="489" height="383" src="https://gitcin.cin.ufpe.br/wrms/kubekepam/raw/master/docs/img/kube_kepam_teorica_resumo.png" />
</p>

* **Monitor:** Este componente coleta em tempo de execução métricas de desempenho e de negócio dos microsserviços. As métricas são coletadas através de API's disponíveis em bancos de dados como o Prometheus ou  InfluxDB. Neste tipo de banco, é possível coletar o último valor da métrica ou agregado passado de valores. 
* **Analisador:** Este componente avalia as métricas coletadas pelo *Monitor* e determina se existem possíveis "sintomas" de uma possível queda no comportamento habitual da aplicação. No geral, existem diversas alternativas para analisar o comportamento do elemento monitorado variando conforme o contexto da aplicação. Nesta solução, é examinada a proporção no uso de recursos da aplicação, assim como feita pelo [HPA Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
* **Planejador:** Este componente avalia os "sintomas" observados pelo *Analisador* e planeja ações que possam redirecionar a aplicação ao seu estado habitual de comportamento. Assim como na análise, diversas alternativas são viáveis para propor ações que tentarão "remover os sintomas presentes". Neste projeto, o *Planejador* calcula  a quantidade de pods necessárias para reajustar o uso dos recursos, assim como feita pelo [HPA Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
* **Executor:** Este componente conhece a quantidade de pods necessárias para cada microsserviço da aplicação disponibilizadas pelo *Planejador*. Sua função, portanto, é apenas atualizar a quantidade de pods por microsserviços através de requisições no Cluster Kubernetes. 


## Arquitetural Implementável

PPara funcionar corretamente o KubeKepam precisa de algumas outras tecnologias/softwares que vão auxiliar na hora de receber métricas e adaptar automaticamente os microsserviços. Logo mais, vamos esclarecer quais são os componentes necessários e o que é utilizado de cada um deles.

##### Online Boutique

Online Boutique é um aplicativo de demonstração de microsserviços nativo da nuvem. Consiste em um aplicativo de comércio eletrônico baseado na web construído em microsserviços de 10 camadas. Nele os usuários podem navegar pelos itens, adicioná-los ao carrinho e comprá-los. 

Em nosso contexto, o Online Boutique faz parte da camada de aplicação, utilizamos ele como um simulador de aplicação real onde podemos gerar uma carga de consumo em cima e realizamos os testes e as demostrações do KubeKepam e seus demais componentes em funcionamento. 

##### Istio
Istio é uma plataforma de service mesh open source que permite controlar a maneira como os microsserviços compartilham dados entre si. O Istio inclui APIs para que ele possa se integrar a qualquer plataforma de geração de registros, sistema de telemetria ou sistema de políticas.

Em nosso contexto, o Istio é utilizado para capturar metricas de negocio, relacionadas as propriedades dos microsserviços.  
Como por exemplo:  
* Tempo de resposta dos microsserviços;
* Tráfego dos microsserviços;

Essas metricas expostas pelo Istio são armazenadas no Prometheus;

##### Kube-Prometheus

É um pacote/biblioteca que inclui uma série de componentes como:
* The Prometheus Operator
* Highly available Prometheus
* Highly available Alertmanager
* Prometheus node-exporter
* Prometheus Adapter for Kubernetes Metrics APIs
* Kube-state-metrics
* Grafana

A ferramenta possui uma pré-configuração que permite coletar métricas de todos os componentes Kubernetes. 
Além disso, permite acesso ao conjunto de painéis do software Grafana contendo a visualização dessas métricas em tempo de execução.

O Kube é responsavel pela coleta de metricas relacionadas a infraestrutura. 
Como por exemplo:
* CPU;
* Memoria;
* Rede;
* Numero de Pods;

Essa coleta é realizada pelo **Kube-state-metrics** e armazenadas do Prometheus.

##### Kubernetes

Segundo o próprio site: "Kubernetes é um produto Open Source utilizado para automatizar a implantação, o dimensionamento e o gerenciamento de aplicativos em contêiner." 
Nós utilizamos o Kubernetes, justamente com essa funcionalidade. Ele é o responsável por receber os comandos do KubeKepam e automatizar a implantação dos contêineres onde estão alocados os microsserviços.

##### Python

Python é uma linguagem de programação de alto nível, amplamente utilizada no mercado. A tecnologia está presente nos códigos do Instagram, Netflix, Spotify, Reddit, Facebook, Google e muitos outros.
Python foi a linguagem de programação escolhida para a implementação do KubeKepam devido a sua versatilidade e facilidade quando o assunto é microsserviços. Python também foi escolhida devida a utilização da **API Python do Kubernetes** que é utilizada em nosso projeto para realizar as adaptações dos microsserviços. 

##### Link das Tecnologias

* [Kubernetes](https://kubernetes.io/pt/)
* [Kube-Prometheus](https://github.com/prometheus-operator/kube-prometheus)
* [Istio](https://istio.io/)
* [Online Boutique](https://github.com/GoogleCloudPlatform/microservices-demo)
* [API Python do Kubernetes](https://github.com/kubernetes-client/python)
* [Python](https://www.python.org/)

## Instalação

##### Softwares adcionais

A instalação do Kube-Kepam exige alguns softwares pré-requisitos. Para aprender como instalar cada software acesse os tutoriais
e os seus scripts de automatização a seguir: 

*  [Como instalar o Kubernetes em Cluster](docs/Kubernetes.md)
*  [Como instalar o KubePrometheus](docs/ISTIO.md)
*  [Como instalar o Istio](docs/ISTIO.md)
*  [Como instalar o OnlineBoutique](docs/OnlineBoutique.md)

##### Como instalar o KubeKepam?  
Para instalar o KubeKepam, siga os seguintes passos:
1. Faça clone do repositorio:   
  `$ git clone https://gitcin.cin.ufpe.br/wrms/kubekepam.git`  
2. Entre no diretorio e execute:  
  `$ pip3 install -r requirements.txt`  
3. Configure as variaveis de ambeinte:  
  **Monitor**: Métricas, Prometheus API URL ISTIO, Prometheus API URL KubeKepam;  
  **Analisador**: Valor desejado para cada métrica coletada no Monitor;  
  **Planejador**: Tempo de espera após uma adaptação;  
  **Executor**: Mover o arquivo `.config` da `$HOME/.kube/config` do Cluster Kubernetes para `$HOME/.kube/config` da máquina executando o KubeKepam;  
  **Mape**: Configurar tempo entre ciclos de execução;  
4. Execute:   
  `$ python3 mape-k.py`
