import yaml
import boto3
import os
import paramiko
import time
ec2=boto3.resource('ec2')
a_yaml_file = open("config.yaml")
values = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
InstanceType=values['server']['instance_type']
ImageId=values['server']['ami_type']
MinCount=values['server']['min_count']
MaxCount=values['server']['max_count']
keyname=values['server']['KeyName']
ec2 = boto3.resource('ec2', region_name="us-west-1")
# volumes = ec2.volumes.all() # If you want to list out all volumes
# # volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['in-use']}]) # if you want to list out only attached volumes
# # [volume for volume in volumes]
# volume_ids = [v.id for v in volumes]
# print(volume_ids)
instance = ec2.create_instances(
    ImageId=ImageId,
     MinCount=MinCount,
     MaxCount=MaxCount,
     InstanceType=InstanceType,
     KeyName=keyname,
    #  DryRun=True
     )

print (instance[0].id)
instance_id=instance[0].id
#=============== creating volume===================
# ebs_vol = ec2.create_volume(
#         Size=size,
#         AvailabilityZone='us-west-1b',
#         VolumeType=type
#     )
# # #============= accesing voluming id===========
# # volumes = ec2.volumes.all() # If you want to list out all volumes
# volume_id = ebs_vol.id
# print(volume_id)
# =========check that the EBS volume has been created successfully==================
# if ebs_vol['ResponseMetadata']['HTTPStatusCode'] == 200:
#     print ("Successfully created Volume! ")


#==========================
#create_and_attach_volume
def create_and_attach_volume(ec2_client, availability_zone, DryRunFlag, device,type,size,instance_id):
    try:
        ebs_vol = ec2.create_volume(
        Size=size,
        AvailabilityZone='us-west-1b',
        VolumeType=type,
        # DryRun=DryRunFlag
        )
    volume_id =ebs_vol['VolumeId']
    print('***Success!! volume:', volume_id, 'created...')

    except Exception as e:
        print('***Failed to create the volume...')
        print(e)
    #===================================
    if volume_id:
        try:
            print('***attaching volume:', volume_id, 'to:', instance_id)
            response= ec2_client.attach_volume(
                Device=device,
                InstanceId=instance_id,
                VolumeId=volume_id,
                # DryRun=DryRunFlag
            )
        #pprint(response)
        except Exception as e:
            print('***Error - Failed to attach volume:', volume_id, 'to the instance:', instance_id)
            print(e)

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
# ===========ssh ing=================
def ssh_connect_with_retry(ssh, ip_address, retries):
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
        './config/ec2-keypair.pem')
    interval = 5
    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        ssh.connect(hostname=ip_address,
                    username='ubuntu', pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)

# get your instance ID from AWS dashboard

# get instance
# ec2 = boto3.resource('ec2', region_name='us-east-1')
instance = ec2.Instance(id=instance_id)
instance.wait_until_running()
current_instance = list(ec2.instances.filter(InstanceIds=[instance_id]))
ip_address = current_instance[0].public_ip_address

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connect_with_retry(ssh, ip_address, 0)

stdin, stdout, stderr = ssh.exec_command(commands)
print('stdout:', stdout.read())
print('stderr:', stderr.read())