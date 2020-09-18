
# KubeKepam
**Descrição**

É uma solução adaptativa que coleta uma variedade de métricas em tempo de execução de Microservices Based Applications (MBAs). A sua arquitetura foi desenvolvida seguindo o modelo MAPE-K bastante utilizado no desenvolvimento de soluções adaptativas.

**O que é o MAPE-K?**

O MAPE-K consiste em um modelo de computação autônoma desenvolvido pela IBM. Esse modelo é composto pelas fases de monitoramento, análise, planejamento e execução em conjunto com uma base de conhecimento. Um modelo genérico MAPE-K é apresentado a seguir: 

![texto](https://gitcin.cin.ufpe.br/wrms/kubekepam/raw/master/docs/img/the_mape-k-control-loop.png)

**Como funciona o MAPE-K do KubeKepam?**

O KubeKepam é uma aplicação composta pelos 4 principais compontes do MAPE-K, sendo eles: monitor, analisador, planejador e executor. A Figura abaixo apresenta o KubeKepam.

![texto](https://gitcin.cin.ufpe.br/wrms/kubekepam/raw/master/docs/img/kube_kepam_teorica_resumo.png)

* **Monitor:** Este componente coleta em tempo de execução métricas de desempenho e de negócio dos microsserviços. As métricas são coletadas através de API's disponíveis em bancos de dados como o Prometheus ou  InfluxDB. Neste tipo de banco, é possível coletar o último valor da métrica ou agregado passado de valores. 
* **Analisador:** Este componente avalia as métricas coletadas pelo *Monitor* e determina se existem possíveis "sintomas" de uma possível queda no comportamento habitual da aplicação. No geral, existem diversas alternativas para analisar o comportamento do elemento monitorado variando conforme o contexto da aplicação. Nesta solução, é examinada a proporção no uso de recursos da aplicação, assim como feita pelo [HPA Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
 * **Planejador:** Este componente avalia os "sintomas" observados pelo *Analisador* e planeja ações que possam redirecionar a aplicação ao seu estado habitual de comportamento. Assim como na análise, diversas alternativas são viáveis para propor ações que tentarão "remover os sintomas presentes". Neste projeto, o *Planejador* calcula  a quantidade de pods necessárias para reajustar o uso dos recursos, assim como feita pelo [HPA Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).
 * **Executor:** Este componente conhece a quantidade de pods necessárias para cada microsserviço da aplicação disponibilizadas pelo *Planejador*. Sua função, portanto, é apenas atualizar a quantidade de pods por microsserviços através de requisições no Cluster Kubernetes. 