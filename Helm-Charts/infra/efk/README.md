    infra/
    ├── efk/
    │   ├── fluent-bit-values.yaml
    │   └── README.md


### REDEPLOY WITH HELM ###
    helm repo add fluent https://fluent.github.io/helm-charts
    helm repo update

    helm upgrade --install fluent-bit fluent/fluent-bit \
    -n efk --create-namespace \
    -f fluent-bit-values.yaml

### Validate after DR restore

    kubectl logs -n efk -l app.kubernetes.io/name=fluent-bit
    curl -k -u elastic:jIJRFJEZHLKLu1wj https://elasticsearch-master:9200/_cat/indices?v


# Fluent Bit DR Guide

## Restore steps
1. Ensure Elasticsearch is running in namespace `efk`
2. Apply Fluent Bit via Helm:
   ```bash
   helm upgrade --install fluent-bit fluent/fluent-bit -n efk --create-namespace -f fluent-bit-values.yaml

3. Confirm logs are flowing:

        kubectl logs -n efk -l app.kubernetes.io/name=fluent-bit
        curl -k -u elastic:<password> https://elasticsearch-master:9200/_cat/indices?v


#### Notes

- ConfigMap is fully managed by Helm

- No manual edits required

- All [OUTPUT] blocks injected via extraOutputs

Let’s lock in a full EFK Disaster Recovery blueprint for you, A — fully declarative, Helm-driven, and reproducible across clusters. This setup will cover:

✅ Elasticsearch

✅ Fluent Bit

✅ Kibana

✅ DR-ready Helm values

✅ Validation steps


    infra/
    └── efk/
        ├── elasticsearch-values.yaml
        ├── fluent-bit-values.yaml
        ├── kibana-values.yaml
        ├── deploy.sh
        └── README.md

