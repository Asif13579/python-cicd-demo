pipeline {

    agent any

    environment {
        IMAGE_NAME = 'ghcr.io/YOUR_GITHUB_USERNAME/python-cicd-demo'
        EC2_USER = 'ubuntu'
        APP_CONTAINER = 'python-cicd-demo'
        APP_PORT = '8000'
    }

    stages {

        // Stage 1: Checkout source code
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code downloaded'
            }
        }

        // Stage 2: Install dependencies
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        // Stage 3: Execute unit tests
        stage('Test') {
            steps {
                sh '''
                    .venv/bin/pytest -v
                '''
            }
        }

        // Stage 4: Build Docker image
        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t $IMAGE_NAME:$BUILD_NUMBER .
                '''
            }
        }

        // Stage 5: Push Docker image
        stage('Push Image') {
            when {
                branch 'main'
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'ghcr-creds',
                        usernameVariable: 'GHCR_USER',
                        passwordVariable: 'GHCR_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x

                        echo "$GHCR_TOKEN" | docker login ghcr.io \
                          -u "$GHCR_USER" --password-stdin

                        docker push $IMAGE_NAME:$BUILD_NUMBER

                        docker logout ghcr.io
                    '''
                }
            }
        }

        // Stage 6: Deploy application to EC2
        stage('Deploy') {
            when {
                branch 'main'
            }

            steps {
                sshagent(credentials: ['ec2-ssh-key']) {

                    withCredentials([
                        string(
                            credentialsId: 'ec2-host',
                            variable: 'EC2_HOST'
                        )
                    ]) {

                        sh '''
                            set -eu

                            ssh -o StrictHostKeyChecking=accept-new \
                                $EC2_USER@$EC2_HOST \
                                "docker pull $IMAGE_NAME:$BUILD_NUMBER"

                            ssh -o StrictHostKeyChecking=yes \
                                $EC2_USER@$EC2_HOST \
                                "docker rm -f $APP_CONTAINER 2>/dev/null || true"

                            ssh -o StrictHostKeyChecking=yes \
                                $EC2_USER@$EC2_HOST \
                                "docker run -d \
                                --restart unless-stopped \
                                --name $APP_CONTAINER \
                                -p $APP_PORT:8000 \
                                $IMAGE_NAME:$BUILD_NUMBER"

                            sleep 5

                            ssh -o StrictHostKeyChecking=yes \
                                $EC2_USER@$EC2_HOST \
                                "curl --fail http://localhost:$APP_PORT/health"
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline failed!'
        }

        always {
            sh 'rm -rf .venv || true'
        }
    }
}