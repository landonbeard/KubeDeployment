def baseImageChoices = ['dockerfile:latest', 'other/image:tag']
def awsCredentialsId = 'your-aws-credentials-id' // The ID of the credentials created in Jenkins

pipeline {
    agent {
        kubernetes {
            customWorkspace 'build'
            defaultContainer 'container-builder'
            yamlFile 'build-pod.yaml'
            workingDir '/home/ci/'
        }
    }//Agent

    //The parameters block allows users to select options for base images, packages, CPU requests, and memory requests
    parameters {
        choice(name: 'BASE_IMAGE', choices: baseImageChoices, description: 'Select the base image')
        string(name: 'PACKAGES', defaultValue: 'default-packages', description: 'Specify packages')
        string(name: 'CPU_REQUEST', defaultValue: '500m', description: 'CPU request for containers')
        string(name: 'MEMORY_REQUEST', defaultValue: '512Mi', description: 'Memory request for containers')
        // Add GPU request parameter if needed
    }
    //The environment block sets the AWS credentials and region
    environment {
        AWS_ACCESS_KEY_ID     = credentials("${awsCredentialsId}.AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = credentials("${awsCredentialsId}.AWS_SECRET_ACCESS_KEY")
        AWS_REGION            = 'us-west-2'
    }
    //The stages block defines the stages of the pipeline
    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                }
            }
        }

        stage('Configure AWS credentials') {
            steps {
                script {
                    withCredentials([
                        [
                            $class: 'AmazonWebServicesCredentialsBinding',
                            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY',
                            credentialsId: awsCredentialsId
                        ]
                    ]) {
                        sh "aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}"
                        sh "aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}"
                        sh "aws configure set default.region ${AWS_REGION}"
                    }
                }
            }
        }//Configure AWS credentials

        stage('Install kubectl') {
            steps {
                script {
                    sh 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"'
                    sh 'chmod +x ./kubectl'
                    sh 'sudo mv ./kubectl /usr/local/bin/kubectl'
                }
            }
        }//Install kubectl

        stage('Deploy to EKS') {
            steps {
                script {
                    sh "kubectl apply -f deployment.yaml --namespace=default --set BASE_IMAGE=${params.BASE_IMAGE}"
                }
            }
        }//Deploy to EKS
    }
}
