# Kubernetes
===> Porque usar o Kubernetes <===

## Instalação do Kubernetes

1. Para instalação do kubernetes é  necessario ter uma instalação limpa do ubunto 2018 ou superior. Basta seguir esses passos para ter o kubernetes instalado.

`$ apt-get update && apt-get install -y apt-transport-https`

`$ curl -fsSL https://get.docker.com | bash`

`$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -`

`$ echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list`

`$ apt-get update`

`$ apt-get install -y kubelet kubeadm kubectl`

2. Antes de iniciar o nosso cluster precisamos desabilitar nossa swap, portanto:

`$ swapoff -a`


3. E comente a entrada referente a swap em seu arquivo fstab:

`$ vim /etc/fstab`

## Iniciação do cluster Kubernetes

`$ mkdir -p $HOME/.kube`

`$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config`

`$ sudo chown $(id -u):$(id -g) $HOME/.kube/config`

`$ kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"`

`$ kubectl get pods -n kube-system`

`$ kubeadm join --token 39c341.a3bc3c4dd49758d5 IP_DO_MASTER:6443 --discovery-token-ca-cert-hash sha256:37092`

`$ kubectl get nodes`
