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

    stage ('Deploy-To-Python') {
      steps {
        sshagent(['python']) {
          sh 'scp -o StrictHostKeyChecking=no target/*.py ubuntu@3.120.192.5:/home/ubuntu/sample/server.py'
        }
      }
    }
    
  }
}
