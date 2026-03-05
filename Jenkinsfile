pipeline {
  agent any

  options { timestamps() }

  environment {
    PYTHON = "C:\\Users\\blegu\\AppData\\Local\\Programs\\Python\\Python314\\python.exe"
  }

  stages {
    stage('Check Python') {
      steps {
        bat """
          "%PYTHON%" --version
          "%PYTHON%" -c "import sys; print(sys.executable)"
        """
      }
    }

    stage('Setup Python') {
      steps {
        bat """
          if exist .venv rmdir /s /q .venv
          "%PYTHON%" -m venv .venv
          .venv\\Scripts\\python -m pip install --upgrade pip
          .venv\\Scripts\\python -m pip install -r requirements.txt
        """
      }
    }

    stage('Install Playwright') {
      steps {
        bat """
          .venv\\Scripts\\python -m playwright install chromium
        """
      }
    }

    stage('Run Tests') {
      steps {
        bat """
          if not exist test-results mkdir test-results
          .venv\\Scripts\\python -m pytest --junitxml=test-results\\junit.xml
        """
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'test-artifacts/**/*, test-results/**/*', allowEmptyArchive: true
      junit testResults: 'test-results/junit.xml', allowEmptyResults: true
    }
  }
}