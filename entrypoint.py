import yaml
import boto3
import os
import paramiko
import time
from create_resources import create_ec2,create_and_attach_volume
from create_keys import checkkey,keyName
from ssh import ssh_connect_with_retry
#==========config  file parsing================
session = boto3.Session()
credentials = session.get_credentials()
access_key = credentials.access_key
secret_key = credentials.secret_key
region_name=session.region_name
#============================ reading variables ============
var_yaml=open("var.yaml")
var = yaml.load(var_yaml, Loader=yaml.FullLoader)
availability_zone=var['availability_zone']
print(availability_zone)
pemfile=var['pemfile']
KeyName=var['KeyName']
#============================ reading config file============
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
    ec2_client = boto3.client('ec2')
    ec2_client.delete_key_pair(KeyName=KeyName)
    print("key-pair already exists")
    keyName(ec2,KeyName,pemfile)
print(pemfile)
os.chmod(pemfile, 400)
# # create ec2 instance
instance_id,ip_address=create_ec2(ec2,ImageId,MinCount,MaxCount,InstanceType,KeyName)
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
    create_and_attach_volume(ec2_client,device,type,size,instance_id,availability_zone)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connect_with_retry(ssh,ip_address,2,'ec2-user',pemfile)
ssh.close()
