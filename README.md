

# Pre-requisties


## Step1: AWS CLI

## Step2: Setup AWS CLI access key in the configuration

# Installation Instructions 

* git clone https://github.com/madhavinamballa/awsEC2_Boto3.git
* update config YAML file based on configurations provide for consumption by application
* Download and install Python 3.8.3
* pip install boto3, paramiko, pyyaml libraries
* Update var.yaml with  availability_zone:  pemfile:  KeyName: 

##  Run "python entrypoint.py" This will do the following

* Deploy the virtual machines
* SSH into the instances as user1 and user2
* Create the two volumes and run other steps in the configuration
* Read from and write to each of two volumes
 



