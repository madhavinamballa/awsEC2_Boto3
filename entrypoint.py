import yaml
import boto3
import os
import paramiko
import time
from create_resources import create_ec2,create_and_attach_volume
from create_keys import checkkey,keyName
from ssh import ssh_connect_with_retry
from user import create_user
conn_args = {
        # 'aws_access_key_id': Your_Access_Key,
        # 'aws_secret_access_key': Your_Secret_Key,
        'region_name': 'us-west-1'
    }
# ~/.aws/credentials
#==========config  file parsing================
session = boto3.Session()
credentials = session.get_credentials()
access_key = credentials.access_key
secret_key = credentials.secret_key
region_name=session.region_name
#============================
var_yaml=open("var.yaml")
var = yaml.load(var_yaml, Loader=yaml.FullLoader)
availability_zone=var['availability_zone']
pemfile=var['pemfile']
KeyName=var['newuser']
#============================
a_yaml_file = open("config.yaml")
values = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
InstanceType=values['server']['instance_type']
ImageId=values['server']['ami_type']
MinCount=values['server']['min_count']
MaxCount=values['server']['max_count']
users=values['server']['users']


ec2=boto3.resource('ec2', 
    region_name=region_name,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,)


# creating keys
if checkkey(KeyName):
    print("creating key-pair")
    keyName(ec2,KeyName,pemfile)
else:
    print("key-pair already exists")
os.chmod(pemfile, 400)
# # create ec2 instance
# instance_id,ip_address=create_ec2(ec2,ImageId,MinCount,MaxCount,InstanceType,KeyName)
instance_id="i-098a76bb35065ff5a"
# # instance = ec2.Instance(id=instance_id)
# # instance_id.wait_until_running()
# # current_instance = ec2.instances.filter(InstanceIds=[instance_id])
# print("===",instance_id)
# # create volume and attach 
ec2_client = boto3.client('ec2')
n=len(values['server']['volumes'])
for i in range(n):
    x=values['server']['volumes'][i]
    li=list(x.values())
    print(li)
    device=x['device']
    size=x['size_gb']
    type=x['type']
    mount=x['mount']
    create_and_attach_volume(ec2_client,device,type,size,instance_id)

# creating user1 user2 
iam = boto3.client('iam')
for i in range(len(users)):
    user=users[i]['login']
    # create_user(user,iam)

# for i in range(len(users)):
#     ssh_connect_with_retry(ssh,'18.144.10.210',2,)
    
ssh into ec2
ip_address = current_instance[0].public_ip_address
# ssh into ec2
ip_address = current_instance[0].public_ip_address

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connect_with_retry(ssh,'18.144.10.210',2,'ec2-user')
ssh.close()