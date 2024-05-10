pipeline {
  agent any
  stages {
    stage ('Initialize') {
      steps {
        sh '''
          echo "PATH= ${PATH}"
          echo "M2_HOME = ${M2_HOME}"
          '''
      }
    }

   stage('Clone Repository') {
            steps {
                git 'https://github.com/DHARMIKR/sample_devsecops.git'
            }
        }
    
    stage ('Deploy-To-Python') {
      steps {
        sshagent(['python']) {
          sh 'scp -o StrictHostKeyChecking=no sample_devsecops/*.py ubuntu@3.120.192.5:/home/ubuntu/sample/server.py'
        }
      }
    }
    
  }
}
