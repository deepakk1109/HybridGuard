pipeline {
    agent any

    environment {
        DOCKER_CREDS         = credentials('dockerhub-creds')
        OPENSHIFT_TOKEN      = credentials('openshift-token')
        OPENSHIFT_SERVER_URL = 'https://api.rm1.0a51.p1.openshiftapps.com:6443'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
                echo "GitHub Code Downloaded Successfully!"
            }
        }

        stage('Docker Build & Push') {
            steps {
                echo "Logging into Docker Hub..."
                sh "echo \$DOCKER_CREDS_PSW | docker login -u \$DOCKER_CREDS_USR --password-stdin"
                sh "docker build -t \$DOCKER_CREDS_USR/hybridguard:latest ."
                sh "docker push \$DOCKER_CREDS_USR/hybridguard:latest"
                echo "Docker Image Built and Pushed Successfully!"
            }
        }

       stage('OpenShift Deploy') {
            steps {
                echo "Deploying to OpenShift..."
                sh "export KUBECONFIG=${WORKSPACE}/.kubeconfig"
                sh "oc login --token=${OPENSHIFT_TOKEN} --server=https://api.rm1.0a51.p1.openshiftapps.com:6443 --insecure-skip-tls-verify=true"
                sh "oc project deepakrishnamoorthi-dev"
                sh "oc delete deployment hybridguard-app --ignore-not-found=true"
                sh "oc delete svc hybridguard-app --ignore-not-found=true"
                sh "oc delete route hybridguard-app --ignore-not-found=true"
                sh "oc delete imagestream hybridguard-app --ignore-not-found=true"
                sh "oc new-app deepak1109/hybridguard:latest --name=hybridguard-app"
                sh "sleep 5"
                sh "oc expose deployment hybridguard-app --port=8080 --target-port=8080 --name=hybridguard-app"
                sh "oc expose svc/hybridguard-app"
                sh "oc rollout status deployment/hybridguard-app --timeout=300s"
                echo "Deployed to OpenShift Successfully!"
            }
        }
    }

    post {
        success {
            echo 'Pipeline Passed Successfully!'
        }
        failure {
            echo 'Pipeline Failed! Check logs.'
        }
    }
}
    
