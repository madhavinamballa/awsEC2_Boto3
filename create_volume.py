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
#============== check keyname exists===========
def checkkey(KeyName):
    ec2 = boto3.client('ec2')
    response = ec2.describe_key_pairs()
    li=response['KeyPairs']
    for i in range(len(li)):
        if li[i]['KeyName'] ==KeyName:
            return False
    return True
#============ create key================
def keyName(ec2,keyname,outputfile):
    # create a file to store the key locally
    outfile = open(outputfile,'w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName=keyname)

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)
#======== create ec2 instance===================
def create_ec2(ec2,ImageId,MinCount,MaxCount,InstanceType,KeyName):
    instance = ec2.create_instances(
        ImageId=ImageId,
        MinCount=MinCount,
        MaxCount=MaxCount,
        InstanceType=InstanceType,
        KeyName=KeyName,
        #  DryRun=True
    )

    print ("creating ec2 instance with : ",instance[0].id)
    instance_id=instance[0].id
    return instance_id 
#=============create_and_attach_volume================
def create_and_attach_volume(ec2, availability_zone, DryRunFlag, device,type,size,instance_id):
    #create
    try:
        ebs_vol = ec2.create_volume(
        Size=size,
        AvailabilityZone='us-west-1b',
        VolumeType=type
        # DryRun=DryRunFlag
        )
        volume_id = ebs_vol.id
        print('***Success!! volume:', volume_id, 'created...')

    except Exception as e:
        print('***Failed to create the volume...')
        print(e)
    #attach
    if volume_id:
        try:
            print('***attaching volume:', volume_id, 'to:', instance_id)
            response= ec2.attach_volume(
                Device=device,
                InstanceId=instance_id,
                VolumeId=volume_id
                # DryRun=DryRunFlag
            )
        #pprint(response)
        except Exception as e:
            print('***Error - Failed to attach volume:', volume_id, 'to the instance:', instance_id)
            print(e)

# ============ssh ing=================
def ssh_connect_with_retry(ssh, ip_address, retries):
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
        filename)
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



# n=len(values['server']['volumes'])
# for i in range(n):
#     x=values['server']['volumes'][i]
#     li=list(x.values())
#     print(li)
#     device=x['device']
#     size=x['size_gb']
#     type=x['type']
#     mount=x['mount']
#     create_and_attach_volume(ec2,'us-west-1b',True,device,type,size,instance_id)
# ===========ssh ing=================
def ssh_connect_with_retry(ssh, ip_address, retries):
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
        'ec2-keypair.pem')
    interval = 5
    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        ssh.connect(hostname=ip_address,
                    username='ec2_user', pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)

# =========driver code======================
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
# ssh into ec2
ip_address = current_instance[0].public_ip_address

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connect_with_retry(ssh, ip_address, 0)

stdin, stdout, stderr = ssh.exec_command(commands)
print('stdout:', stdout.read())
print('stderr:', stderr.read())
# create users
stdin, stdout, stderr = ssh.exec_command("sudo adduser -d /home/mynewuser newuser")
stdin, stdout, stderr = ssh.exec_command("sudo chmod 700 /home/mynewuser/.ssh")
stdin, stdout, stderr = ssh.exec_command("sudo chmod 600 /home/mynewuser/.ssh/authorized_keys")
# stdin, stdout, stderr = ssh.exec_command("sudo echo "ssh key" >> /home/mynewuser/.ssh/authorized_keys")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
ssh.close()