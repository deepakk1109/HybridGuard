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

        // Bypassing the network drop stage temporarily to update OpenShift config
        /*
        stage('Docker Build & Push') {
            steps {
                echo "Logging into Docker Hub..."
                sh "echo \$DOCKER_CREDS_PSW | docker login -u \$DOCKER_CREDS_USR --password-stdin"
                sh "docker build --no-cache -t \$DOCKER_CREDS_USR/hybridguard:latest ."
                sh "docker push \$DOCKER_CREDS_USR/hybridguard:latest"
            }
        }
        */

        stage('Deploy to OpenShift') {
            steps {
                echo "Logging into OpenShift Cluster..."
                sh "oc login ${OPENSHIFT_SERVER_URL} --token=\$OPENSHIFT_TOKEN --insecure-skip-tls-verify"
                
                echo "Injecting AWS S3 Variables safely using Jenkins Credentials..."
                
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'MY_AWS_ACC'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'MY_AWS_SEC')
                ]) {
                    sh """
                        oc set env deployment/hybridguard-app \
                        AWS_ACCESS_KEY_ID="\$MY_AWS_ACC" \
                        AWS_SECRET_ACCESS_KEY="\$MY_AWS_SEC" \
                        AWS_S3_BUCKET_NAME="hybridguard-storage-9927"
                    """
                }
                
                echo "Triggering Rollout to apply new AWS configurations..."
                sh "oc rollout restart deployment/hybridguard-app"
                sh "oc rollout status deployment/hybridguard-app --timeout=60s"
            }
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
