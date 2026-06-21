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
                sh '''
                    export KUBECONFIG=$WORKSPACE/.kubeconfig
                    
                    # 1. Login to OpenShift
                    oc login --token=sha256~awArwFlNkyS12g8iOuYny31_vExu3uM-CWA8Fdyj8WI --server=https://api.rm1.0a51.p1.openshiftapps.com:6443
                    
                    # 2. Switch to your project namespace
                    oc project deepakrishnamoorthi-dev
                    
                    # 3. Clean up existing deployment if it exists
                    oc delete deployment hybridguard-app || true
                    oc delete svc hybridguard-app || true
                    oc delete route hybridguard-app || true
                    
                    # 4. Deploy your new image from Docker Hub
                    oc new-app deepak1109/hybridguard:latest --name=hybridguard-app
                    
                    # 5. Expose the service to generate a live public URL
                    oc expose svc/hybridguard-app
                '''
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
