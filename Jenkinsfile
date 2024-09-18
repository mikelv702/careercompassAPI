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
				sh 'python3 -m pip install ruff'
				sh 'python3 -m ruff check'
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
					if(env.BRANCH_NAME == 'main') {
                    docker.withRegistry('https://992382387335.dkr.ecr.us-west-2.amazonaws.com', 'ecr:us-west-2:ecr-aws-creds') {
                    app.push("${env.BUILD_NUMBER}")
                    app.push("latest")
					} else {echo "Development Branch!"}
					
                    }
                }
            }
        }
    }
}
