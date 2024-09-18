pipeline {
    agent {label 'lab-builder'}
    options {
        skipStagesAfterUnstable()
    }
    stages {
         stage('Clone repository') { 
            steps { 
                script{
                checkout scm
                }
            }
        }
		stage('Lint') {
			steps {
				ruff check
			}
		}
        stage('Build') { 
            steps { 
                script{
                 app = docker.build("careercompass/api")
                }
            }
        }
        stage('Test'){
            steps {
                 echo 'Empty'
				 echo 'Running Tests'
            }
        }
        stage('Deploy') {
            steps {
                script{
                        docker.withRegistry('https://992382387335.dkr.ecr.us-west-2.amazonaws.com', 'ecr:us-west-2:ecr-aws-creds') {
                    app.push("${env.BUILD_NUMBER}")
                    app.push("latest")
                    }
                }
            }
        }
    }
}
