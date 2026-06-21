# OpenShift Setup Guide — HybridGuard

## 1. Get Sandbox Access

Go to https://developers.redhat.com/developer-sandbox → "Start your sandbox"
→ login with Red Hat account → wait ~2-3 min for provisioning.

## 2. Login via oc CLI

Copy the login command from the OpenShift web console (top-right → "Copy login command"):

```bash
oc login --token=YOUR_TOKEN --server=https://api.sandbox-m2.ll9k.p1.openshiftapps.com:6443
oc whoami
oc project deepakkrishnamoorthi
```

## 3. Apply Manifests

```bash
oc apply -f openshift/configmap.yaml
# create the aws-credentials secret first - see docs/AWS_SETUP.md
oc apply -f openshift/deployment.yaml
oc apply -f openshift/service.yaml
oc apply -f openshift/route.yaml
oc apply -f openshift/servicemonitor.yaml
```

## 4. Verify

```bash
oc get pods -n deepakkrishnamoorthi
oc get route hybridguard -n deepakkrishnamoorthi -o jsonpath='{.spec.host}'

curl https://<route-host>/health
curl -X POST https://<route-host>/predict -d '{"features":[0.5,1.2,-0.3,2.1,0.8]}'
```

## 5. View Metrics

OpenShift Console → Observe → Metrics → query `predictions_total` or `anomalies_total`.
