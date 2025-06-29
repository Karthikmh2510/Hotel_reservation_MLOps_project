pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "geometric-team-461617-u4"
        GCLOUD_PATH ="/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning GitHub repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning GitHub repo to Jenkins.....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Karthikmh2510/Hotel_reservation_MLOps_project.git']])
                }
            }
        }

        stage('Setting up Virtual Environment and Installing Dependencies'){
            steps{
                script{
                    echo 'Setting up Virtual Environment and Installing Dependencies.....'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                    }
            }
        }

        stage('Building and pushing Docker image to GCR'){
            steps{
                withCredientials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pushing Docker image to GCR.....'
                        sh '''
                      
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quite

                        docker build -t gcr.io/${GCP_PROJECT}/hotel-reservation:latest .
                        docker push gcr.io/${GCP_PROJECT}/hotel-reservation:latest
                        '''
                    }
                }
            }
        }

    }
}

