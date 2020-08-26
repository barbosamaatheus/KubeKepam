# Online Boutique

## Tutorial de implantação do OnlineBoutique em um Cluster Kubernetes Local

**Requisitos para essa instalação:**
* Cluster Kubernetes instalado (Tutorial disponível em: [Como montar seu Cluster Kubernetes](docs/Kubernetes.md))

## Implantação do OnlineBoutique

1. Clone o repositorio para a maquina Master do Cluster.

     `$ git clone https://github.com/GoogleCloudPlatform/microservices-demo.git`
     
2. Entre na pasta clonada.
     `$ cd nome_da_pasta`

3. Implante a MBA no Kubernetes. 

     `$ kubectl apply -f ./release/kubernetes-manifests.yaml`

3. Verifique se todos os pods foram implantados corretamente.

     `$ watch kubectl get pods`
     
     Se tudo ocorrer bem, o comando retornará como saida: 
     ```bash
     
     NAME                                     READY   STATUS    RESTARTS   AGE
     adservice-5c9c7c997f-bp5nl               1/1     Running   0          5m
     cartservice-6d99678dd6-1vmf5             1/1     Running   1          5m
     checkoutservice-779cb9bfdf-5fkhg         1/1     Running   0          5m
     currencyservice-5db6c7d559-qnjmx         1/1     Running   0          5m
     emailservice-5c47dc87bf-67shv            1/1     Running   0          5m
     frontend-5fcb8cdcdc-n7tth                1/1     Running   0          5m
     paymentservice-6564cb7fb9-x84vd          1/1     Running   0          5m
     productcatalogservice-5db9444549-whhdk   1/1     Running   0          5m
     recommendationservice-5d5f794679-7rgct   1/1     Running   0          5m
     redis-cart-57bd646894-crjc5              1/1     Running   0          5m
     shippingservice-f47755f97-kkdcj          1/1     Running   0          5m
     
     ```

4. Identifique a porta na qual a aplicação está disponível.

     `$ kubectl get service/frontend-external`
    
     Se tudo ocorrer bem, o comando retornará como saida: 
     ```
     NAME                TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
     frontend-external   LoadBalancer   10.105.128.254   <pending>     80:32558/TCP   5m
     ```
     
5. Acesse a aplicação no navegador usando o IP do Master e a porta do microsserviço frontend.

     `https://ip_maquina_master:porta_microsserviço_frontend`


Para mais informações, acesse a documentação da MBA neste link [aqui](https://github.com/GoogleCloudPlatform/microservices-demo).