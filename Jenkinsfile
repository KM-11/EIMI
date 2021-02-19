pipeline {
    agent any
    stages {

        stage('Check dependencies') {
            steps {
                sh 'python3 -m safety check -r requirements.txt'
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
            }
            
        }
        stage('run docker image') {
            steps{
                sh 'docker container run -d -p 8000:8000 --name eimi-ci eimi' 
            }
        }
//      
         stage('test web works') {
            steps{
                sh 'sleep 3'
                sh 'ab -c 100 -n 1000 http://127.0.0.1:8000/'
                
            }
        }
        
        stage('clean container'){
            steps{
                sh 'docker container stop eimi-ci'
                sh 'docker container rm eimi-ci'
            }
        }
    }
}
