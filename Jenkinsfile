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
        sh '''
            export KUBECONFIG=${WORKSPACE}/.kubeconfig
            oc login --token=${OPENSHIFT_TOKEN} --server=https://api.rm1.0a51.p1.openshiftapps.com:6443
            oc project deepakrishnamoorthi-dev
            oc delete deployment hybridguard-app --ignore-not-found=true
            oc delete svc hybridguard-app --ignore-not-found=true
            oc delete route hybridguard-app --ignore-not-found=true
            oc delete imagestream hybridguard-app --ignore-not-found=true
            oc new-app deepak1109/hybridguard:latest --name=hybridguard-app
            sleep 5
            oc expose deployment hybridguard-app --port=8080 --target-port=8080 --name=hybridguard-app
            oc expose svc/hybridguard-app
            oc rollout status deployment/hybridguard-app --timeout=300s
        '''
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
stage('OpenShift Deploy') {
    steps {
        sh '''
            export KUBECONFIG=${WORKSPACE}/.kubeconfig
            oc login --token=${OPENSHIFT_TOKEN} --server=https://api.rm1.0a51.p1.openshiftapps.com:6443
            oc project deepakrishnamoorthi-dev
            oc delete deployment hybridguard-app --ignore-not-found=true
            oc delete svc hybridguard-app --ignore-not-found=true
            oc delete route hybridguard-app --ignore-not-found=true
            oc delete imagestream hybridguard-app --ignore-not-found=true
            oc new-app deepak1109/hybridguard:latest --name=hybridguard-app
            sleep 5
            oc expose deployment hybridguard-app --port=8080 --target-port=8080 --name=hybridguard-app
            oc expose svc/hybridguard-app
            oc rollout status deployment/hybridguard-app --timeout=300s
        '''
    }
}
