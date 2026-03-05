pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://your-repo-url.git'
            }
        }

        stage('Setup Python') {
            steps {
                bat '''
                python -m venv .venv
                .venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Install Playwright') {
            steps {
                bat '''
                .venv\\Scripts\\python -m playwright install chromium
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                .venv\\Scripts\\pytest
                '''
            }
        }

    }

    post {
        always {
            archiveArtifacts artifacts: 'test-artifacts/**/*', allowEmptyArchive: true
        }
    }
}