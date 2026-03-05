pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/master']],
                        userRemoteConfigs: [[
                        url: 'https://github.com/Nairod010/playwright-demo.git',
                        credentialsId: 'github-pat'
                    ]]
                ])
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