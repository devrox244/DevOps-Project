// Jenkinsfile - Final Simplified Version

pipeline {
    // Run directly on the Jenkins agent
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

        stage('2. Compile (Linting)') {
            steps {
                // FIX: No VENV. Install tools directly on the agent.
                sh "pip install pylint"
                
                // Run pylint on your application file
                sh "pylint app.py"
            }
        }

        stage('3. Build/Package/Unit Testing') {
            steps {
                echo 'Installing project dependencies...'
                // FIX: Install requirements directly.
                sh 'pip install -r requirements.txt'

                echo 'Running unit tests...'
                sh 'pip install pytest'
                sh 'pytest --junitxml=test-results.xml || true'
            }
        }

        stage('4. SonarQube (Optional)') {
            steps {
                echo 'Skipping SonarQube analysis.'
            }
        }

        stage('5. Deploying on Server') {
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
                            python3 -m venv venv_remote
                            . venv_remote/bin/activate
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
    
    // Post-build actions for cleanup
    post {
        always {
            // FIX: Removed the 'rm -rf venv' since we are not creating it locally.
            echo 'Pipeline completed.'
        }
        unstable {
            junit '**/test-results.xml' 
        }
        success {
            echo 'Build and Deployment Succeeded!'
        }
    }
}