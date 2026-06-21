pipeline {
    agent any
    environment {
        DOCKERHUB = credentials('dockerhub-creds')
        AWS = credentials('aws-creds')
        OC_TOKEN = credentials('openshift-token')
        IMAGE = 'deepakk1109/hybridguard:latest'
    }
    stages {
        stage('Checkout') {
            steps { 
                git branch: 'main', url: 'https://github.com/deepakk1109/HybridGuard.git' 
            }
        }
        stage('Build Docker Image') {
            steps { 
                sh 'docker build -t $IMAGE .' 
            }
        }
        stage('Push to Docker Hub') {
            steps {
                // Docker Hub-ல் லாகின் செய்து இமேஜை புஷ் செய்யும் பகுதி
                sh 'echo $DOCKERHUB_PSW | docker login -u $DOCKERHUB_USR --password-stdin'
                sh 'docker push $IMAGE'
            }
        }
        stage('Deploy to OpenShift') {
            steps {
                // OpenShift Sandbox-ல் லாகின் செய்து டெப்ளாய் செய்யும் பகுதி
                sh 'oc login --token=$OC_TOKEN --server=https://api.sandbox.openshiftapps.com:6443'
                sh 'oc apply -f openshift/'
                sh 'oc rollout restart deployment/hybridguard -n deepakkrishnamoorthi'
            }
        }
    }
    post {
        success { 
            echo 'Deployment successful!' 
        }
        failure { 
            echo 'Pipeline Failed! Check logs.' 
        }
    }
}
