# Istio

## Baixae o Istio

1.  Acesse a página de [versão](https://github.com/istio/istio/releases/tag/1.7.0) do Istio para baixar o arquivo de instalação para seu sistema operacional ou faça o download e extraia a versão mais recente automaticamente (Linux ou macOS):

`$ curl -L https://istio.io/downloadIstio | sh -`

> O comando acima baixa a versão mais recente (numericamente) do Istio. Você pode passar variáveis ​​na linha de comando para baixar uma versão específica ou substituir a arquitetura do processador. Por exemplo, para baixar o Istio 1.6.8 para a arquitetura x86_64, execute `curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.6.8 TARGET_ARCH=x86_64 sh -`.
2. Mova para o diretório de pacotes do Istio. Por exemplo, se o pacote for **istio-1.7.0**:

`$ cd istio-1.7.0`

3. Adicione o **istioctl** cliente ao seu caminho (Linux ou macOS):

`$ export PATH=$PWD/bin:$PATH` ou você também pode usar `$ sudo install istioctl /usr/local/bin/istioctl`.

## Instale o Istio
Na instalação do Istio, você pode optar por perfis de configuração diferentes, abaixo mostramos outros perfis existentes.  
Os componentes marcados como X são instalados em cada perfil:

| **Core components** | default | demo | minimal | remote |
| ------ | ------ | ------ | ------ | ------ |
| **istio-egressgateway** |   | X |  |  | 
| **istio-ingressgateway** | X | X |  |  |
| **istiod** | X | X | X |  | 

Para personalizar ainda mais o Istio e instalar complementos, você pode adicionar uma ou mais opções `--set <key>=<value>` no comando `istioctl install` que você usará para instalar o Istio.  


Para esta instalação, usamos o perfil de configuração **demo**. Ele foi selecionado para ter um bom conjunto de padrões para teste.  

1. Execute o comando: 
`$ istioctl install --set profile=demo`

Você receberá como saida: 
```bash
✔ Istio core installed
✔ Istiod installed
✔ Egress gateways installed
✔ Ingress gateways installed
✔ Installation complete
```
2. Adicione um rótulo de namespace para instruir o Istio a injetar automaticamente proxies secundários do Envoy ao implantar seu aplicativo posteriormente:
`$ kubectl label namespace default istio-injection=enabled`

Você receberá como saida: 
`namespace/default labeled`

Pronto, agora você já deve está com tudo pronto.
para mais informações, consulte a [documentação oficial](https://istio.io/latest/docs/setup/getting-started/).

## Implante a aplicação 

Estamos usando o Online Botique como aplicação de demostraçaõ. Acesse a [documentação](docs/OnlineBoutique.md) para saber com implantar