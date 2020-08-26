# Cluster Kubernetes

## Tutorial de instalação do Cluster Kubernetes


Cluster Kubernetes instalado (Tutorial disponível em: Como montar seu Cluster Kubernetes)

**Requisitos para essa instalação:**
* No mínimo duas máquinas instaladas com sistemas operacionais Linux que são baseados no Debian, p. ex.: [Ubuntu Server 20](https://ubuntu.com/download/server)


## Instalando componentes básicos

1. Para instalar o Kubernetes em cluster, todas as máquinas precisam desses elementos básicos:

    * Atualizar as referências de software do sistema para instalar o pacote apt-transport-https
     
        `$ apt-get update && apt-get install -y apt-transport-https`
         
    * Instalar o Docker 
    
        `$ curl -fsSL https://get.docker.com | bash`
        
    * Instalar os pacotes básicos do Kubernetes

        `$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -`

        `$ echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list`

        `$ apt-get update && apt-get install -y kubelet kubeadm kubectl`
        
    * Desativar a memória swap ativa atualmente (caso ativada)

        `$ swapoff -a`
        
    * Impedir que o swap seja ativado permantemente.
    Acesse o arquivo /etc/fstab e comente a linha que refere-se a swap. 
    No exemplo a seguir, é o arquivo do Ubuntu Server 20.04. 
         
        Acesse o arquivo usando: 
        `$ vim /etc/fstab`
        
        ```
        Arquivo original
        # <file system> <mount point>   <type>  <options>       <dump>  <pass>
        # / was on /dev/xvda2 during curtin installation
        /dev/disk/by-uuid/3e5fecd8-e275-41b5-96a1-3d3f86d2122c / ext4 defaults 0 0
        /swap.img      none    swap    sw      0       0
        ```
        
        Comente a linha que referencia o swap (basta inserir um # no inicio da linha) e salve o arquivo. 
        
        ```
        Arquivo modificado
        # <file system> <mount point>   <type>  <options>       <dump>  <pass>
        # / was on /dev/xvda2 during curtin installation
        /dev/disk/by-uuid/3e5fecd8-e275-41b5-96a1-3d3f86d2122c / ext4 defaults 0 0
        #/swap.img  

## Criando e configurando o Cluster Kubernetes

Nesse momento, é necessário determinar as funções de cada máquina. 
Ou seja, quais máquinas serão Masters ou Workers. 
Além disso, certos comandos são efetuados apenas em máquinas do tipo Worker ou Master.
Portanto, fique atente para não usar um comando para uma máquina Master em uma máquina Worker. 

1. Inicialize o Cluster Kubernetes na máquina (Master). 

     `$ kubeadm init --apiserver-advertise-address ip_maquina_master`

2. Colete o comando kubeadm join disponível no final da instalação. 
    * Esse comando será utilizado posteriormente nos Workers. 
      Esse comando sempre varia para cada instalação do Kubernetes, mas o que deve ser salvo é algo desse tipo:

         `$ kubeadm join --token 39c341.a3bc3c4dd49758d5 IP_DO_MASTER:6443 --discovery-token-ca-cert-hash sha256:37092`

3. Crie uma pasta .kube e copie o arquivo padrao de instalação do Kubernetes para a pasta $HOME do seu usuário (Master).

     `$ mkdir -p $HOME/.kube`
     
     `$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config`
     
4. Insira as permissões necessárias ao arquivo (Master).
     
     `$ sudo chown $(id -u):$(id -g) $HOME/.kube/config`

5. Implante um gerenciar de um rede para permitir a comunição das maquinas dentro da rede (Máquina Master).

     `$ kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"`
     
6. Liste e veja os pods rede implantados (Master).

     `$ kubectl get pods -n kube-system`

7. Insira os Workers no Cluster Kubernetes usando o comando coletado no passo 2 (Workers).

     `$ kubeadm join --token 39c341.a3bc3c4dd49758d5 IP_DO_MASTER:6443 --discovery-token-ca-cert-hash sha256:37092`
     
8. Visualize se os workers foram inseridos no cluster (Master).

     `$ watch kubectl get nodes`


Se necessário, consulte tambem este [tutorial](https://www.linuxtips.io/post/descomplicando-o-kubernetes-02) para utilização do kubernetes.

Para mais informações acesse a documentação oficial do [Kubernetes](https://kubernetes.io/).
