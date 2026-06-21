pipeline {
    agent any

    environment {
        DOCKER_CREDS         = credentials('dockerhub-creds')
        OPENSHIFT_TOKEN      = credentials('openshift-token')
        // 1. Defined your OpenShift Server URL here so the variable works
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
                // Switched to single quotes to completely fix the trailing quote issue
                sh 'oc login --token=$OPENSHIFT_TOKEN --server=$OPENSHIFT_SERVER_URL --insecure-skip-tls-verify'
                echo "Deployed to OpenShift Successfully!"
            }
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
