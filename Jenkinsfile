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
                sh 'rm trufflehog || true'
                sh 'docker run gesellix/trufflehog --json https://github.com/DHARMIKR/sample_devsecops.git >> trufflehog'
                sh 'cat trufflehog'
            }
        }

        stage('Start Python Server') {
            steps {
                script {
                    // Start the Python server in the background
                    sh 'nohup python3 Password_Management_System.py &'
                    // Wait for the server to start
                    sleep 10
                }
            }
        }

        stage('Stop Python Server') {
            steps {
                script {
                    // Stop the Python server
                    sh 'pkill -f Password_Management_System.py'
                }
            }
        }
    }

}
