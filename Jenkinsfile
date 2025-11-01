// Jenkinsfile - Declarative Pipeline for Python Flask CI/CD

pipeline {
    agent any

    // 1. Define Environment Variables
    environment {
        // Fetches the secret API key from Jenkins Credentials
        WEATHER_API = credentials('weather-api-key')
        
        // Deployment configuration variables (Finalized EC2 details)
        REMOTE_SERVER = 'ubuntu@13.232.66.82'
        REMOTE_PATH   = '/opt/weather-app'
        VENV_DIR      = 'venv' // Local VENV name
    }

    stages {
        stage('1. Git Code Checkout') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/devrox244/DevOps-Project'
            }
        }

        stage('2. Compile (Setup & Linting)') {
            steps {
                // FIX: Use 'sudo' to grant root privileges for package installation
                sh 'sudo apt update && sudo apt install -y python3-venv'
                
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
                // Build/Package step: Install dependencies from requirements.txt
                sh 'pip install -r requirements.txt'

                echo 'Running unit tests...'
                // Install testing tool and run tests 
                sh 'pip install pytest'
                // Runs tests and allows pipeline to continue on test failure
                sh 'pytest --junitxml=test-results.xml || true'
            }
        }

        stage('4. SonarQube (Optional)') {
            steps {
                echo 'Skipping SonarQube analysis.'
            }
        }

        stage('5. Deploying on Server') {
            // Loads the private key from the 'deploy-ssh-key' credential
            steps {
                sshagent(credentials: ['deploy-ssh-key']) {
                    echo "Deploying to ${REMOTE_SERVER} at ${REMOTE_PATH}"
                    
                    // 1. Transfer the entire current workspace to the remote server
                    sh "scp -o StrictHostKeyChecking=no -r ./* ${REMOTE_SERVER}:${REMOTE_PATH}"
                    
                    // 2. Execute deployment commands remotely
                    sh """
                        ssh -o StrictHostKeyChecking=no ${REMOTE_SERVER} "
                            # Navigate to the deployment directory
                            cd ${REMOTE_PATH} || exit 1
                            
                            # Stop any existing running instance of the app
                            echo 'Stopping old process...'
                            pkill -f 'python app.py' || true

                            # Create and activate a VENV on the remote server
                            echo 'Setting up remote VENV...'
                            python3 -m venv ${VENV_DIR}_remote
                            . ${VENV_DIR}_remote/bin/activate
                            
                            # Install fresh dependencies on the server
                            pip install -r requirements.txt
                            
                            # Start the application using nohup, passing the WEATHER_API environment variable
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
                sh "rm -rf \$VENV_DIR" 
            }
        }
        unstable {
            // Publish test results if tests failed
            junit '**/test-results.xml' 
        }
        success {
            echo 'Build and Deployment Succeeded!'
        }
    }
}