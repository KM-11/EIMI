pipeline {
    agent any
    stages {

        stage('Check dependencies') {
            steps {
                sh 'python3 -m safety check -r requirements.txt || exit 0'
            }
        }

        stage('Static Code Analyisis') {
            steps {
                sh 'python3 -m bandit -r ./ || exit 0'
            }
        }
        
        stage('buid docker image') {
            steps{
                sh 'docker image build -t eimi .'  
                sh 'docker container run -p 8000:8000 eimi'
            }
            
        }

//       
    }
}
