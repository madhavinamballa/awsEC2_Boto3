#Pre-requisties

Step1: AWS Account

Step2: AWS CLI

Step3: Setup AWS CLI access key in the configuration

# AwsEC2_Boto3
step1: git clone https://github.com/madhavinamballa/awsEC2_Boto3.git

Step2: update config YAML file based on configurations provide for consumption by application

Step3:  Download and install Python 3.8.3

Step4:  pip install boto3, paramiko, pyyaml libraries

Step4: Update var.yaml with  availability_zone:  pemfile:  KeyName: 

Step5:  Run "python entrypoint.py" This will do the following

Deploy the virtual machines

SSH into the instances as user1 and user2

Create the two volumes and run other steps in the configuration

Read from and write to each of two volumes
 



