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
def keyName(ec2,keyname,pemfile):
    outfile = open('new-keypair.pem','w')
    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName=keyname)

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)