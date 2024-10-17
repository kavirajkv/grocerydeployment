pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = 'dockerhub-credential' 
        DOCKER_IMAGE_NAME = 'jenkinstest'
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/kavirajkv/grocerydeployment.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dir('/grocery-store') {
                        sh "sudo docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ."
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "echo $DOCKER_PASSWORD | sudo docker login -u $DOCKER_USERNAME --password-stdin"

                        sh "sudo docker tag ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} $DOCKER_USERNAME/${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                        
                        sh "sudo docker push $DOCKER_USERNAME/${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Docker image built and pushed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
