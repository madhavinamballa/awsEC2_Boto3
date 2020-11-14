import yaml
import boto3
import os
import paramiko
import time
#==========config  file parsing================
filename='new-keypair.pem'
a_yaml_file = open("config.yaml")
values = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
InstanceType=values['server']['instance_type']
ImageId=values['server']['ami_type']
MinCount=values['server']['min_count']
MaxCount=values['server']['max_count']
KeyName=values['server']['KeyName']
# ec2 = boto3.resource('ec2', region_name="us-west-1")
#=============create_and_attach_volume================
def create_and_attach_volume(ec2, availability_zone, DryRunFlag, device,type,size,instance_id):
    #create
 
    ebs_vol = ec2.create_volume(
        Size=size,
        AvailabilityZone='us-west-1b',
        VolumeType=type
        )
    volume_id =ebs_vol['VolumeId']
    print('***Success!! volume:', volume_id, 'created...')
    # #attach
    # if volume_id:
    #     try:
    #         print('***attaching volume:', volume_id, 'to:', instance_id)
    #         response= ec2.attach_volume(
    #             Device=device,
    #             InstanceId=instance_id,
    #             VolumeId=volume_id
    #             # DryRun=DryRunFlag
    #         )
    #     #pprint(response)
    #     except Exception as e:
    #         print('***Error - Failed to attach volume:', volume_id, 'to the instance:', instance_id)
    #         print(e)

# ============ssh ing=================


     
ec2 = boto3.resource('ec2', region_name="us-west-1")
# creating keys
instance_id='i-013f0826fe7ca775c'
instance = ec2.Instance(id=instance_id)
instance.wait_until_running()
current_instance = list(ec2.instances.filter(InstanceIds=[instance_id]))
# create volume and attach 
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
    create_and_attach_volume(ec2_client,'us-west-1b',True,device,type,size,instance_id)
