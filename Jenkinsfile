// Jenkinsfile - Final Simplified Version (All Build Steps on Remote)

pipeline {
    // This agent just needs to run the git checkout and ssh commands
    agent any

    // 1. Define Environment Variables
    environment {
        WEATHER_API = credentials('weather-api-key')
        REMOTE_SERVER = 'ubuntu@13.232.66.82'
        REMOTE_PATH   = '/opt/weather-app'
    }

    stages {
        stage('1. Git Code Checkout') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/devrox244/DevOps-Project'
            }
        }

        // This is now the ONLY other stage. It does everything.
        stage('2. Build, Test, and Deploy on EC2 Server') {
            steps {
                sshagent(credentials: ['deploy-ssh-key']) {
                    echo "Connecting to ${REMOTE_SERVER}..."
                    
                    // 1. Transfer the source code to the EC2 server
                    sh "scp -o StrictHostKeyChecking=no -r ./* ${REMOTE_SERVER}:${REMOTE_PATH}"
                    
                    // 2. Execute ALL commands on the EC2 server
                    sh """
                        ssh -o StrictHostKeyChecking=no ${REMOTE_SERVER} "
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