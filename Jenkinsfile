pipeline {
    agent any

    environment {
        GITHUB_REPO = 'https://github.com/DHARMIKR/sample_devsecops.git'
        GIT_BRANCH = 'main'
        APP_PORT = '80'  // Port your Python app runs on
        SONARQUBE_SCANNER_HOME = tool name: 'sonar', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
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
                sh 'docker run --dns 8.8.8.8 gesellix/trufflehog --json https://github.com/DHARMIKR/sample_devsecops.git >> trufflehog'
                sh 'cat trufflehog'
            }
        }

        stage('Source Composition Analysis'){
            steps{
                sh 'rm owasp* || true'
                sh 'wget https://raw.githubusercontent.com/devopssecure/webapp/master/owasp-dependency-check.sh'
                sh 'chmod +x owasp-dependency-check.sh'
                sh 'bash owasp-dependency-check.sh'
            }
        }

        stage('SAST') {
            steps {
                withSonarQubeEnv('sonar') { // Use the configured SonarQube server
                    sh "${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=devsecops -Dsonar.sources=. -Dsonar.language=python -Dsonar.sourceEncoding=UTF-8 -Dsonar.login=sqa_b521b254d233f95eafa3f949a296fb4a120923b3"
                }
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

        stage('DAST') {
            steps {
                sh 'docker run -t ictu/zap2docker-weekly zap-baseline.py -t http://127.0.0.1:5000/api/ || true'
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
