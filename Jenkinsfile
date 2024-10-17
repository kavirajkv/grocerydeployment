pipeline {
    agent any

    environment {
        // DOCKER_CREDENTIALS = 'dockerhub-credential' 
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
            }
        }

        stage('pushing image to dockerhub'){
            steps{
                script{
                    def credentials = credentials('dockerhub-credential')
                    def username = credentials.split(':')[0]
                    def password = credentials.split(':')[1]

                    sh "docker login -u ${username} -p ${password}"

                    sh "docker tag ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ${username}/${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"

                    sh "docker push ${username}/${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"

                }    
            }
        }

        stage('deleting the image'){
            steps{
                sh "docker rmi kavirajkv/${DOCKER_IMAGE_NAME}"
                sh "docker rmi ${DOCKER_IMAGE_NAME}"
            }
        }
    }


    post {
        success {
            echo 'Docker image built and pushed successfully and deleted image locally'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
