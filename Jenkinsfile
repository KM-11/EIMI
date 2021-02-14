pipeline {
    agent any
    stages {

        stage('Check dependencies') {
            steps {
                sh 'python3 -m safety -r requirements.txt'
            }
        }

        stage('Static Code Analyisis') {
            steps {
                sh 'python3 -m bandit -r ./'
            }
        }

//       
    }
}
