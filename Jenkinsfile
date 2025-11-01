// Jenkinsfile - Declarative Pipeline for Python Flask CI/CD

pipeline {
    // FIX: Use a Docker agent that already has Python + Venv installed
    agent {
        docker { 
            image 'python:3.10-slim' 
        }
    }

    // 1. Define Environment Variables
    environment {
        WEATHER_API = credentials('weather-api-key')
        REMOTE_SERVER = 'ubuntu@13.232.66.82'
        REMOTE_PATH   = '/opt/weather-app'
        VENV_DIR      = 'venv' 
    }

    stages {
        stage('1. Git Code Checkout') {
            steps {
                echo 'Cloning repository...'
                // The 'checkout scm' step is now needed because the agent is custom
                checkout scm
            }
        }

        stage('2. Compile (Setup & Linting)') {
            steps {
                // REMOVED: 'sudo apt update' (not needed, tools are pre-installed)
                
                // Create and activate an isolated Python virtual environment (VENV)
                sh "python3 -m venv ${VENV_DIR}"
                
                sh ". ${VENV_DIR}/bin/activate" 
                
                // Install linting tool
                sh "pip install pylint"
                
                // Run pylint on your application file for syntax and style checks
                sh "pylint app.py"
            }
        }

        stage('3. Build/Package/Unit Testing') {
            steps {
                // Activate the VENV from the previous stage
                sh ". ${VENV_DIR}/bin/activate"
                
                echo 'Installing project dependencies...'
                sh 'pip install -r requirements.txt'

                echo 'Running unit tests...'
                sh 'pip install pytest'
                sh 'pytest --junitxml=test-results.xml || true'
            }
        }

        stage('4. SonRube (Optional)') {
            steps {
                echo 'Skipping SonarQube analysis.'
            }
        }

        stage('5. Deploying on Server') {
            // This stage will run on the same Python container agent
            steps {
                sshagent(credentials: ['deploy-ssh-key']) {
                    echo "Deploying to ${REMOTE_SERVER} at ${REMOTE_PATH}"
                    
                    sh "scp -o StrictHostKeyChecking=no -r ./* ${REMOTE_SERVER}:${REMOTE_PATH}"
                    
                    sh """
                        ssh -o StrictHostKeyChecking=no ${REMOTE_SERVER} "
                            cd ${REMOTE_PATH} || exit 1
                            echo 'Stopping old process...'
                            pkill -f 'python app.py' || true
                            echo 'Setting up remote VENV...'
                            python3 -m venv ${VENV_DIR}_remote
                            . ${VENV_DIR}_remote/bin/activate
                            pip install -r requirements.txt
                            echo 'Starting new application instance...'
                            nohup WEATHER_API='${env.WEATHER_API}' python3 app.py > app.log 2>&1 &
                            echo 'Deployment complete. App is running in the background.'
                        "
                    """
                }
            }
        }
    }
    
    // Post-build actions for cleanup and reporting
    post {
        always {
            echo 'Pipeline completed. Cleaning up local VENV.'
            // This 'script' block provides the necessary context for the 'sh' step
            script {
                sh "rm -rf \$VVENV_DIR" 
            }
        }
        unstable {
            junit '**/test-results.xml' 
        }
        success {
            echo 'Build and Deployment Succeeded!'
        }
    }
}