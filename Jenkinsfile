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
                sh '''cd grocery-store
                    docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} .'''

                sh "docker images"
                sh "docker ps -a"
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
