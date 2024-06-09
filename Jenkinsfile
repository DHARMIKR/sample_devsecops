pipeline {
    agent any

    environment {
        GITHUB_REPO = 'https://github.com/DHARMIKR/sample_devsecops.git'
        GIT_BRANCH = 'main'
        APP_PORT = '80'  // Port your Python app runs on
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: "${GIT_BRANCH}", url: "${GITHUB_REPO}"
            }
        }

        stage('Check Git Secrets') {
            steps {
                sh 'trufflehog --regex --entropy=False --json --repo . > trufflehog_report.json'
                archiveArtifacts artifacts: 'trufflehog_report.json', allowEmptyArchive: true
            }
        }

        stage('Start Python Server') {
            steps {
                script {
                    // Start the Python server in the background
                    sh 'nohup python3 server.py &'
                    // Wait for the server to start
                    sleep 10
                }
            }
        }

        stage('Stop Python Server') {
            steps {
                script {
                    // Stop the Python server
                    sh 'pkill -f server.py'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/*.html, **/*.json', allowEmptyArchive: true
            junit 'reports/**/*.xml'  // If any tests produce JUnit XML reports
        }
    }
}
