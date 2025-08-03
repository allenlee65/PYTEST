pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'pytest-automation'
        SENDER_EMAIL = credentials('sender-email')
        EMAIL_PASSWORD = credentials('email-password')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    try {
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").inside(
                            '--shm-size=2g -v /var/run/docker.sock:/var/run/docker.sock'
                        ) {
                            sh '''
                                pytest uiTests/automation_exercise_test.py \
                                    -v \
                                    --reruns=3 \
                                    --reruns-delay=2 \
                                    --html=reports/report.html \
                                    --self-contained-html \
                                    --junit-xml=reports/junit.xml
                            '''
                        }
                    } catch (Exception e) {
                        currentBuild.result = 'UNSTABLE'
                        echo "Tests failed but continuing pipeline: ${e.getMessage()}"
                    }
                }
            }
        }
        
        stage('Archive Results') {
            steps {
                script {
                    docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").inside {
                        sh 'cp -r reports/* ${WORKSPACE}/reports/ || true'
                    }
                }
                
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Pytest HTML Report'
                ])
                
                junit 'reports/junit.xml'
            }
        }
        
        stage('Send Email Report') {
            steps {
                script {
                    docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").inside(
                        "-e SENDER_EMAIL=${SENDER_EMAIL} -e EMAIL_PASSWORD=${EMAIL_PASSWORD}"
                    ) {
                        sh '''
                            python -c "
from uiTests.automation_exercise_test import TestResultCollector
TestResultCollector.send_test_report_email()
                            "
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
            script {
                docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").remove()
            }
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        unstable {
            echo 'Pipeline is unstable!'
        }
    }
}