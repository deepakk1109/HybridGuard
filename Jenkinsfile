pipeline {
    agent any

    environment {
        DOCKER_CREDS = credentials('dockerhub-creds')
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
    } // <-- This closes the stages block

    post {
        success {
            echo 'Pipeline Passed Successfully! Application is running locally on port 8080.'
        }
        failure {
            echo 'Pipeline Failed! Check configuration parameters.'
        }
    }
}
