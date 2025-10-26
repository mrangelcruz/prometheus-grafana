## Python app stress testing

__Hit the login page a few times__

    for i in {1..10}; do curl -s http://192.168.1.219:30500/login > /dev/null; done

__Hit the dashboard endpoint a few times__

    for i in {1..5}; do curl -s http://192.168.1.219:30500/dashboard > /dev/null; done

__Hit dashboard several times__

    for i in {1..10}; do curl -s http://192.168.1.219:30500/dashboard > /dev/null; done

__Hit home (which redirects to login, so optional)__

    for i in {1..5}; do curl -s http://192.168.1.219:30500/ > /dev/null; done


## Create a Debug Pod

-> start a debug pod with curl already installed

    kubectl run debug-curl --rm -i --tty --image=curlimages/curl --restart=Never -- sh


-> inside the debug pod: 

    curl -v http://python-logger.default.svc.cluster.local:5000/metrics | head

## Exec commands to a running pod

    kubectl exec -it python-logger-6dd866db45-dr28j -- netstat -tlnp | grep 5000

    kubectl exec -it python-logger-6dd866db45-dr28j -- ss -tlnp
    
    kubectl exec -it python-logger-6dd866db45-dr28j -- sh -c "curl -v http://localhost:5000/metrics | head"


