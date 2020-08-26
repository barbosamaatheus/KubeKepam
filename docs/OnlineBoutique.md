# Online Boutique

## Passos para a instalação do Online Boutique da Google em um Cluster Kubernetes Local

1. Clone o repositorio para sua maquina.

`$ git clone https://github.com/GoogleCloudPlatform/microservices-demo.git`

2. Implante os microsserviços no Kubernetes. 

`$ kubectl apply -f ./release/kubernetes-manifests.yaml`

3. Verifique se todos os pods estão funcionando corretamente:

`$ watch kubectl get pods`

4. Encontre a porta que a aplicação está rodando:

`$ kubectl get service/frontend-external`


Por fim voce pode visualizar a documentação acessando a pagina neste link [aqui](https://github.com/GoogleCloudPlatform/microservices-demo).