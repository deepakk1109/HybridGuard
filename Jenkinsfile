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



       stage('Build Docker Image') {
    steps {
        sh 'docker build -t hybridguard:latest .'
    }
}
stage('Run locally') {
    steps {
        
        sh 'docker stop hybridguard-app || true'
        sh 'docker rm hybridguard-app || true'
        sh 'docker run -d -p 8080:80 --name hybridguard-app hybridguard:latest'
    }
}

    post {
        success {
            echo 'Pipeline Passed Successfully! AWS Credentials synced to OpenShift!'
        }
        failure {
            echo 'Pipeline Failed! Check configuration parameters.'
        }
    }
}
