pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-dockerhub-username/python-realtime-app:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/akhilmukka/python-realtime-app-monitoring.git'
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE, "./app").push()
                }
            }
        }

        stage('Deploy to Stage') {
            steps {
                sh """
                kubectl apply -f k8s/stage/deployment.yaml
                kubectl apply -f k8s/stage/service.yaml
                """
            }
        }

        stage('Manual Approval for Review') {
            steps {
                input message: 'Deploy to Review environment?', ok: 'Approve'
            }
        }

        stage('Deploy to Review') {
            steps {
                sh """
                kubectl apply -f k8s/review/deployment.yaml
                kubectl apply -f k8s/review/service.yaml
                """
            }
        }

        stage('Manual Approval for Production') {
            steps {
                input message: 'Deploy to Production?', ok: 'Yes, deploy to prod'
            }
        }

        stage('Deploy to Production') {
            steps {
                sh """
                kubectl apply -f k8s/prod/deployment.yaml
                kubectl apply -f k8s/prod/service.yaml
                """
            }
        }
    }

    post {
        success {
            echo "✅ Deployment Pipeline completed successfully!"
        }
        failure {
            echo "❌ Deployment failed. Please check the logs."
        }
    }
}
