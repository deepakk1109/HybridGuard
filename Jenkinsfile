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
                // --no-cache வச்சு லோக்கல் கேச் எரரைத் தவிர்க்கிறோம்!
                sh "docker build --no-cache -t \$DOCKER_CREDS_USR/hybridguard:latest ."
                sh "docker push \$DOCKER_CREDS_USR/hybridguard:latest"
                echo "Docker Image Built and Pushed Successfully!"
            }
        }

        stage('Deploy to OpenShift') {
            environment {
                AWS_ACCESS = credentials('AWS_ACCESS_KEY_ID')
                AWS_SECRET = credentials('AWS_SECRET_ACCESS_KEY')
            }
            steps {
                echo "Logging into OpenShift..."
                // முதலில் ஓபன்ஷிஃப்ட்டில் செக்யூராக லாகின் செய்கிறோம்
                sh "oc login ${OPENSHIFT_SERVER_URL} --token=\$OPENSHIFT_TOKEN --insecure-skip-tls-verify"
                
                echo "Setting AWS Credentials in OpenShift Deployment..."
                // சாவிகளை செக்யூராக ஓபன்ஷிஃப்ட்டில் ஏற்றி, எஸ்3 பக்கெட்டையும் இணக்கிறோம்
                sh "oc set env deployment/hybridguard-app AWS_ACCESS_KEY_ID=\$AWS_ACCESS AWS_SECRET_ACCESS_KEY=\$AWS_SECRET AWS_S3_BUCKET_NAME='hybridguard-storage-9927'"
                
                echo "Forcing Rollout to take fresh image and env changes..."
                sh "oc rollout restart deployment/hybridguard-app"
                sh "oc rollout status deployment/hybridguard-app --timeout=60s"
            }
        }
    }

    post {
        success {
            echo 'Pipeline Passed Successfully! Deepak, go ahead and test your curl now!'
        }
        failure {
            echo 'Pipeline Failed! Check logs for specific errors.'
        }
    }
}
