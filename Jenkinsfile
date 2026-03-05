pipeline {
  agent any

  options { timestamps() }

  stages {
    stage('Check Python') {
      steps {
        bat '''
          echo Checking Python availability...
          where py || echo py not found
          where python || echo python not found
          py -V || echo py -V failed
          python -V || echo python -V failed
        '''
      }
    }

    stage('Setup Python') {
      steps {
        bat '''
          if exist .venv rmdir /s /q .venv

          where py >nul 2>nul
          if %errorlevel%==0 (
            py -m venv .venv
          ) else (
            where python >nul 2>nul
            if %errorlevel%==0 (
              python -m venv .venv
            ) else (
              echo ERROR: Python not found for Jenkins user. Install Python for all users and/or add to PATH.
              exit /b 1
            )
          )

          .venv\\Scripts\\python -m pip install --upgrade pip
          .venv\\Scripts\\python -m pip install -r requirements.txt
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
          if not exist test-results mkdir test-results
          .venv\\Scripts\\python -m pytest --html=report.html --self-contained-html --junitxml=test-results\\junit.xml
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'report.html, test-artifacts/**/*, test-results/**/*', allowEmptyArchive: true
      junit testResults: 'test-results/junit.xml', allowEmptyResults: true
    }
  }
}