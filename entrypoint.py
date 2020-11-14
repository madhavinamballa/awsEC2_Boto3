import yaml
import boto3
import os
import paramiko
import time
from create_resources import create_ec2,create_and_attach_volume
from create_keys import checkkey,keyName


#==========config  file parsing================
availability_zone='us-west-1b'
filename='new-keypair.pem'
a_yaml_file = open("config.yaml")
values = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
InstanceType=values['server']['instance_type']
ImageId=values['server']['ami_type']
MinCount=values['server']['min_count']
MaxCount=values['server']['max_count']
KeyName=values['server']['KeyName']


ec2 = boto3.resource('ec2', region_name="us-west-1")
# creating keys
if checkkey(KeyName):
    print("creating key-pair")
    keyName(ec2,KeyName,filename)
else:
    print("key-pair already exists")
os.chmod("ec2-keypair.pem", 400)
# create ec2 instance
instance_id=create_ec2(ec2,ImageId,MinCount,MaxCount,InstanceType,KeyName)
#instance_id="i-013f0826fe7ca775c"
#instance = ec2.Instance(id=instance_id)
# instance_id.wait_until_running()
# current_instance = ec2.instances.filter(InstanceIds=[instance_id])
print("===",instance_id)
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


# ssh into ec2
# ip_address = current_instance[0].public_ip_address
