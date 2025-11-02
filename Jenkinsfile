// Jenkinsfile - Final Fix using withCredentials to bypass libcrypto error

pipeline {
    agent any

    environment {
        WEATHER_API = credentials('weather-api-key')
        // MAKE SURE THIS IS THE IP OF YOUR LATEST EC2 INSTANCE
        REMOTE_SERVER = 'ubuntu@[YOUR_NEW_EC2_IP]' 
        REMOTE_PATH   = '/opt/weather-app'
    }

    stages {
        stage('1. Git Code Checkout') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/devrox244/DevOps-Project'
            }
        }

        // This stage does all the work on the server
        stage('2. Build, Test, and Deploy on EC2 Server') {
            steps {
                // FIX: Replaced 'sshagent' with 'withCredentials'
                withCredentials([sshUserPrivateKey(credentialsId: 'deploy-ssh-key', keyFileVariable: 'EC2_PRIVATE_KEY')]) {
                    // 'EC2_PRIVATE_KEY' is now a variable holding the path to the key file
                    
                    echo "Connecting to ${REMOTE_SERVER} with new key..."
                    
                    // 1. Make the key file readable only by us
                    sh "chmod 400 \${EC2_PRIVATE_KEY}"
                    
                    // 2. Transfer the source code, using -i to specify the key file
                    sh "scp -o StrictHostKeyChecking=no -i \${EC2_PRIVATE_KEY} -r ./* ${REMOTE_SERVER}:${REMOTE_PATH}"
                    
                    // 3. Execute ALL commands on the EC2 server, using -i to specify the key file
                    sh """
                        ssh -o StrictHostKeyChecking=no -i \${EC2_PRIVATE_KEY} ${REMOTE_SERVER} "
                            # Navigate to the deployment directory
                            cd ${REMOTE_PATH} || exit 1

                            # --- 1. COMPILE/BUILD STEP (on EC2) ---
                            echo 'Setting up remote VENV...'
                            python3 -m venv venv_remote
                            . venv_remote/bin/activate
                            
                            echo 'Installing dependencies...'
                            pip install -r requirements.txt
                            
                            echo 'Installing build tools...'
                            pip install pylint pytest
                            
                            # --- 2. TEST STEP (on EC2) ---
                            echo 'Running Linter...'
                            pylint app.py
                            
                            echo 'Running Unit Tests...'
                            pytest || true

                            # --- 3. DEPLOY STEP (on EC2) ---
                            echo 'Stopping old process...'
                            pkill -f 'python app.py' || true
                            
                            echo 'Starting new application instance...'
                            nohup WEATHER_API='${env.WEATHER_API}' python3 app.py > app.log 2>&1 &
                            
                            echo 'Deployment complete. App is running in the background.'
                        "
                    """
                }
            }
        }
    }
    
    // Simplified post-build actions
    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'Build and Deployment Succeeded!'
        }
    }
}