# Istio

## Tutorial de instalação do Istio

**Requisitos para essa instalação:**
* Cluster Kubernetes instalado (Tutorial disponível em: [Como montar seu Cluster Kubernetes](teste.com))



## Instalação do Istio


1.  Acesse a página de [versões](https://github.com/istio/istio/releases) do Istio para baixar o arquivo de instalação 
    para seu sistema operacional ou faça o download e extraia a versão mais recente de forma automatica:

      `$ curl -L https://istio.io/downloadIstio | sh -`

> O comando acima baixa a versão mais recente (numericamente) do Istio. Você pode passar variáveis na linha de comando 
para baixar uma versão específica ou substituir a arquitetura do processador. Por exemplo, para baixar o Istio 1.6.8 para 
a arquitetura x86_64, execute `$ curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.6.8 TARGET_ARCH=x86_64 sh -`.

2. Entre no novo diretório do Istio disponível na sua máquina. Por exemplo, se o pacote for **istio-1.7.0**:

      `$ cd istio-1.7.0`

3.  Instale o binário do Istio no sistema:

      `$ sudo install istioctl /usr/local/bin/istioctl`

> No site oficial, o Istio indica inserir o caminho da pasta que foi feita download no PATH do sistema. Porém, esse
comando apenas funciona até a reinicialização do sistema. Após a reinicialização, é necessário refazer novamente o comando. 
Além disso, qualquer mudança da localização da pasta do Istio, também exige a inserção da nova localização do Isto. O comando acima
sugerido pelo tutorial é executado uma única vez e permite a exclusão da pasta. 

4.  Exclua a pasta do Istio. Por exemplo, se a pasta for **istio-1.7.0**::

      `$ cd .. ; rm istio-1.7.0 -r`

## Implantação do Istio

Na implantação do Istio, você pode optar por perfis de configuração diferentes. Logo abaixo, é apresentado brevemente os perfis existentes. 
Uma descrição mais abrangente dos componentes presentes em cada perfil está disponível neste [link](https://istio.io/latest/docs/setup/additional-setup/config-profiles/). 
Os componentes marcados como X são instalados em cada perfil:

| **Core components** | default | demo | minimal | remote |
| ------ | ------ | ------ | ------ | ------ |
| **istio-egressgateway** |   | X |  |  | 
| **istio-ingressgateway** | X | X |  |  |
| **istiod** | X | X | X |  | 

Para instalar um dos perfils do Istio, é necessário usar o comando `$ istioctl install` com o parâmetro`--set <key>=<value>`. 
Para a instalação para o projeto dessa disciplina, foi necessário utilizar o perfil de configuração **demo**. 
Ele foi selecionado devido as ferramentas presentes neste perfil de implantação como o prometheus, grafana e Kiali.

1. Execute o comando: 
      `$ istioctl install --set profile=demo`

     Se tudo ocorrer bem, a instalação retornará como saida: 
     ```bash
     ✔ Istio core installed
     ✔ Istiod installed
     ✔ Egress gateways installed
     ✔ Ingress gateways installed
     ✔ Installation complete
     ```
2. Informe ao Istio em qual namespace do Kubernetes estará implantada a MBA que se deseja monitorar: 

     `$ kubectl label namespace default istio-injection=enabled`

     Se tudo ocorrer bem, a instalação retornará como saida:  
     ```namespace/default labeled```

Pronto, agora o Cluster Kubernetes já contém as ferramentas básicas necessárias para monitorar as MBAs implantadas nele.
para mais informações, consulte a [documentação oficial](https://istio.io/latest/docs/setup/getting-started/).

## Como implanatar uma MBA no Kubernetes?

Nos experimentos da disciplina, a equipe está utilizando o Online Botique como aplicação de demostração. 
Acesse o [guia de instalação do Online Boutique](docs/OnlineBoutique.md) para saber como implantar.