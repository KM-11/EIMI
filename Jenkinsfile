pipeline {
    agent any
    stages {

        stage('Build docker image') {
            steps {
                sh 'docker-compose build
            }
        }

        stage('Scan docker image') {
            steps {
                sh 'clair-scanner --ip 192.168.1.120 webserver || exit 0'
                sh 'clair-scanner --ip 192.168.1.120 mysqlserver || exit 0'
            }
        }

//       
    }
}
