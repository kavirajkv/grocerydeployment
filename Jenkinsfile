pipeline{
    agent any
    stages{
        stage("init"){
            steps{
                echo "initial stage"
            }
           
        }
        stage("test"){
            steps{
                echo "test"
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
            echo "failed"
        }
    }
}