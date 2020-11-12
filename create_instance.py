import yaml
import boto3
import os
def checkkey(keyname):
    ec2 = boto3.client('ec2')
    response = ec2.describe_key_pairs()
    li=response['KeyPairs']
    for i in range(len(li)):
        if li[i]['KeyName'] ==keyname:
            return False
    return True
def keyName(ec2,keyname):
    # create a file to store the key locally
    outfile = open('ec2-keypair.pem','w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName=keyname)

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)

ec2=boto3.resource('ec2')
a_yaml_file = open("config.yaml")
values = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
InstanceType=values['server']['instance_type']
ImageId=values['server']['ami_type']
MinCount=values['server']['min_count']
MaxCount=values['server']['max_count']
keyname=values['server']['KeyName']
device=values['server']['volumes'][0]['device']
size=values['server']['volumes'][0]['size_gb']
type=values['server']['volumes'][0]['type']
if checkkey(keyname):
    print("creating key-pair")
    keyName(ec2,keyname)
else:
    print("key-pair already exists")
os.chmod("ec2-keypair.pem", 400)
# keyName(ec2,keyname)
instance_new = ec2.create_instances(
     ImageId=ImageId,
     MinCount=MinCount,
     MaxCount=MaxCount,
     InstanceType=InstanceType,
     KeyName=keyname
     
 )


li=[]
for instance in ec2.instances.all():
     
    li.append(instance.id)
print(li[0])

ebs_vol = ec2.create_volume(
        Size=size,
        AvailabilityZone='us-west-1',
        type=type
    )

volume_id = ebs_vol['VolumeId']
print(volume_id)
# check that the EBS volume has been created successfully
if ebs_vol['ResponseMetadata']['HTTPStatusCode'] == 200:
    print ("Successfully created Volume! " + volume_id)
# attaching EBS volume to our EC2 instance
attach_resp = client.attach_volume(
    VolumeId=volume_id,
    InstanceId=li[0],
    Device=device
    )

