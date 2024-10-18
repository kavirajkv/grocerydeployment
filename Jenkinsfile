pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'jenkinstest'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
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
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credential', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin"

                        sh "docker tag ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"

                        sh "docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    }

                }    
            }
        }

        stage('deleting the image'){
            steps{
                script{
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credential', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "docker rmi ${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                        sh "docker rmi ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
                
            }
        }

        stage('clone the deployment repo'){
            steps{
                git url: 'https://github.com/kavirajkv/grocery-cd.git' , branch: 'main', credentialsid: 'github-credential'
                sh 'ls'
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
