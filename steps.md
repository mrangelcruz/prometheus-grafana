#### Assumption:
- kubernetes controllers and workers already set up

$ k get pods -A


    NAMESPACE      NAME                                                READY   STATUS    RESTARTS         AGE
    efk            elasticsearch-master-0                              1/1     Running   0                5d5h
    efk            fluent-bit-dqc58                                    1/1     Running   0                5d2h
    efk            fluent-bit-qjmsv                                    1/1     Running   0                5d2h
    kube-flannel   kube-flannel-ds-565xm                               1/1     Running   0                7d19h
    kube-flannel   kube-flannel-ds-rmfxf                               1/1     Running   0                7d19h
    kube-flannel   kube-flannel-ds-tzc5z                               1/1     Running   4 (5m27s ago)    7d19h
    kube-system    coredns-5cc59f8848-96txt                            1/1     Running   4 (5m27s ago)    14d
    kube-system    coredns-5cc59f8848-wbvkt                            1/1     Running   4 (5m27s ago)    14d
    kube-system    etcd-ac-dream                                       1/1     Running   9 (5m27s ago)    15d
    kube-system    kube-apiserver-ac-dream                             1/1     Running   9 (5m27s ago)    15d
    kube-system    kube-controller-manager-ac-dream                    1/1     Running   10 (5m27s ago)   15d
    kube-system    kube-proxy-46mn8                                    1/1     Running   4 (5m27s ago)    13d
    kube-system    kube-proxy-pd88s                                    1/1     Running   2 (10d ago)      13d
    kube-system    kube-proxy-q7hzg                                    1/1     Running   1 (8d ago)       9d
    kube-system    kube-scheduler-ac-dream                             1/1     Running   10 (5m27s ago)   15d
    monitoring     grafana-6f84ddbdcc-wfjdz                            1/1     Running   2 (5m27s ago)    44h
    monitoring     my-grafana-7d575d4fd4-qh57n                         1/1     Running   0                44h
    monitoring     prometheus-kube-state-metrics-64464d99cd-p48sf      1/1     Running   2 (5m27s ago)    44h
    monitoring     prometheus-prometheus-node-exporter-4plns           1/1     Running   0                7d15h
    monitoring     prometheus-prometheus-node-exporter-gzv8k           1/1     Running   3 (5m27s ago)    7d15h
    monitoring     prometheus-prometheus-node-exporter-q4tkx           1/1     Running   0                7d15h
    monitoring     prometheus-prometheus-pushgateway-cd9c95968-j2qdm   1/1     Running   2 (5m27s ago)    44h
    monitoring     prometheus-server-7699b7d474-nwlmj                  2/2     Running   0                44h

$ k get nodes -o wide

    NAME            STATUS   ROLES           AGE   VERSION    INTERNAL-IP     EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION       CONTAINER-RUNTIME
    ac-dream        Ready    control-plane   15d   v1.29.15   192.168.1.219   <none>        KDE neon User Edition            6.14.0-32-generic    containerd://1.7.28
    k8-controller   Ready    worker          9d    v1.29.2    192.168.1.99    <none>        Ubuntu 22.04.5 LTS               6.8.0-85-generic     containerd://1.7.28
    raspberrypi     Ready    worker          14d   v1.29.15   192.168.1.95    <none>        Debian GNU/Linux 12 (bookworm)   6.12.34+rpt-rpi-v8   containerd://1.6.20

## ACCESS GRAFANA

- Port Forward

        $k port-forward -n monitoring pod/grafana-6f84ddbdcc-wfjdz 3001:3000
        
        Forwarding from 127.0.0.1:3001 -> 3000
        Forwarding from [::1]:3001 -> 3000
        Handling connection for 3001

__PASSWORD RECOVERY__

username: admin

If you forget what the password is

go inside pod:

    kubectl exec -it -n monitoring pod/grafana-6f84ddbdcc-wfjdz -- /bin/sh


while inside pod:

    grafana-cli admin reset-admin-password admin

('admin' is the new password)

Enter the new password at http://localhost:3001

## ACCESS PROMETHEUS

- find out the ports in the container

$ k get svc -n monitoring

    NAME                                  TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
    grafana                               ClusterIP   10.98.216.177    <none>        80/TCP           6d
    my-grafana                            NodePort    10.110.92.49     <none>        3000:30300/TCP   7d15h
    prometheus-kube-state-metrics         ClusterIP   10.101.201.108   <none>        8080/TCP         7d16h
    prometheus-prometheus-node-exporter   ClusterIP   10.101.240.228   <none>        9100/TCP         7d16h
    prometheus-prometheus-pushgateway     ClusterIP   10.111.53.36     <none>        9091/TCP         7d16h
    prometheus-server                     NodePort    10.97.138.119    <none>        9090:30090/TCP   7d16h


So, for the prometheus-server, I will forward port 9090.

    $ k port-forward -n monitoring pod/prometheus-server-7699b7d474-nwlmj  9090:9090

    Forwarding from 127.0.0.1:9090 -> 9090
    Forwarding from [::1]:9090 -> 9090
    Handling connection for 9090

## If you need to rebuild python app

    cd /home/angelcruz/repos/prometheus-grafana/python_app/app

    docker build -t mrangelcruz1960/python-logger:latest .
    docker push mrangelcruz1960/python-logger:latest
    kubectl rollout restart deployment python-logger

However, we will deploy this to a raspberrypi; hence, it has to be built for that architecture.

    docker buildx create --use

    docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t mrangelcruz1960/python-logger:latest \
    --push .

check the docker manifest after

    docker manifest inspect mrangelcruz1960/python-logger:latest
