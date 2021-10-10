pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh """
                python3 -m venv venv_api_2
                source venv_api_2/bin/activate
                pip install -r requirements.txt
                """
            }
        }
        stage('Lint') {
            steps {
                sh """
                source venv_api_2/bin/activate
                pylint net_api
                """
            }
        }
        stage('Unittest') {
            steps {
                sh """
                source venv_api_2/bin/activate
                python manage.py test
                """
            }
        }
        post {
            always {
                junit '*.xml'
            }
        }
    }
}