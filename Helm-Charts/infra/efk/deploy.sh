#!/bin/bash
set -e

helm repo add elastic https://helm.elastic.co
helm repo add fluent https://fluent.github.io/helm-charts
helm repo update

kubectl create namespace efk || true

helm upgrade --install elasticsearch elastic/elasticsearch -n efk -f elasticsearch-values.yaml
helm upgrade --install fluent-bit fluent/fluent-bit -n efk -f fluent-bit-values.yaml
helm upgrade --install kibana elastic/kibana -n efk -f kibana-values.yaml
