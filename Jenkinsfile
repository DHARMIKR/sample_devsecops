pipeline {
    agent any

    environment {
        GITHUB_REPO = 'https://github.com/DHARMIKR/sample_devsecops.git'
        GIT_BRANCH = 'main'
        SONARQUBE_SERVER = 'http://127.0.0.1:9000'
        ZAP_DOCKER_IMAGE = 'owasp/zap2docker-stable'
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

        stage('Source Composition Analysis') {
            steps {
                sh '/home/ubuntu/dependency-check/bin/dependency-check.sh --project "PythonApp" --scan . --format "ALL" --out dependency-check-report'
                archiveArtifacts artifacts: 'dependency-check-report/*', allowEmptyArchive: true
            }
        }

        stage('Static Application Security Testing (SAST)') {
            steps {
                script {
                    withSonarQubeEnv('SonarQube') { 
                        sh 'sonar-scanner'
                    }
                }
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

        stage('Dynamic Application Security Testing (DAST)') {
            steps {
                sh "docker run --rm -v $(pwd):/zap/wrk:rw -t ${ZAP_DOCKER_IMAGE} zap-baseline.py -t http://127.0.0.1:${APP_PORT} -r zap_report.html"
                archiveArtifacts artifacts: 'zap_report.html', allowEmptyArchive: true
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
