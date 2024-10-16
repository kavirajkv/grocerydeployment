def groovy
pipeline{
    agent any
    stages{
        stage("init"){
            script{
                groovy=load "script.groovy"
            }
        }
        stage("test"){
            steps{
                echo "test"
                groovy.hello()
            }
        
        }
        stage("build"){
            steps{
                echo "this is ${env.BRANCH_NAME}"
            }
        }
    }
    post{
        always{
            echo "finished"
        }
        success{
            echo "its success"
        }
        failure{
            echo "faild"
        }
    }
}