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
                sh """
  oc login --token=\$OPENSHIFT_TOKEN --server=https://api.rm1.0a51.p1.openshiftapps.com:6443 --insecure-skip-tls-verify=true
"""
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
