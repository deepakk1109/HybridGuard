# Jenkins Setup Guide — HybridGuard

## 1. Run Jenkins (Docker, free, self-hosted)

```bash
docker run -d --name jenkins \
  -p 8081:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open `http://localhost:8081`, paste the password, install suggested plugins,
create an admin user.

## 2. Install Required Plugins

Manage Jenkins → Plugins → Available, install:
- Docker Pipeline
- GitHub Integration
- Credentials Binding Plugin

## 3. Add Credentials

Manage Jenkins → Credentials → Add Credentials:

| ID | Type | Value |
|---|---|---|
| `dockerhub-creds` | Username/Password | Docker Hub login |
| `aws-creds` | Username/Password | AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY |
| `openshift-token` | Secret text | output of `oc whoami -t` |

## 4. Create the Pipeline Job

New Item → Pipeline → name it `HybridGuard` → Pipeline script from SCM →
Git → repo URL `https://github.com/deepakk1109/HybridGuard.git` →
Script Path: `Jenkinsfile`.

## 5. GitHub Webhook (auto-trigger on push)

GitHub repo → Settings → Webhooks → Add webhook:
- Payload URL: `http://YOUR_JENKINS_URL:8081/github-webhook/`
- Content type: `application/json`
- Trigger: Just the push event

In the Jenkins job config → Build Triggers → check
"GitHub hook trigger for GITScm polling".

## 6. Test

```bash
git commit --allow-empty -m "trigger jenkins"
git push origin main
```

Watch the pipeline run at `http://localhost:8081/job/HybridGuard/`.
