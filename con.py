import yaml
import boto3
import os
import paramiko
import time
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
# # 
# print(len(values['server']['volumes']))
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
ec2 = boto3.resource('ec2', region_name="us-west-1")

# instance = ec2.create_instances(
#     ImageId=ImageId,
#      MinCount=MinCount,
#      MaxCount=MaxCount,
#      InstanceType=InstanceType,
#      KeyName=keyname
#     #  DryRun=True
#      )

# print (instance[0].id)
# instance_id=instance[0].id
instance_id="i-0ea46ff576956087f"
def execute_commands_on_linux_instances(client, commands, instance_ids):
    """Runs commands on remote linux instances
    :param client: a boto/boto3 ssm client
    :param commands: a list of strings, each one a command to execute on the instances
    :param instance_ids: a list of instance_id strings, of the instances on which to execute the command
    :return: the response from the send_command function (check the boto3 docs for ssm client.send_command() )
    """

    resp = client.send_command(
        DocumentName="AWS-RunShellScript", # One of AWS' preconfigured documents
        Parameters={'commands': commands},
        InstanceIds=instance_id,
    )
    return resp

# Example use:
commands = ['echo "hello world"']
def ssh_connect_with_retry(ssh, ip_address, retries):
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
        'ec2-keypair.pem')
    # privkey=keyname
    interval = 5
    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        ssh.connect(hostname=ip_address,
                    username='ec2-user', pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)

# get your instance ID from AWS dashboard

# get instance
instance = ec2.Instance(id=instance_id)
instance.wait_until_running()
current_instance = list(ec2.instances.filter(InstanceIds=[instance_id]))
ip_address = current_instance[0].public_ip_address

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connect_with_retry(ssh, ip_address, 0)

stdin, stdout, stderr = ssh.exec_command("sudo adduser -d /home/mynewuser newuser")
stdin, stdout, stderr = ssh.exec_command("sudo chmod 700 /home/mynewuser/.ssh")
stdin, stdout, stderr = ssh.exec_command("sudo chmod 600 /home/mynewuser/.ssh/authorized_keys")
stdin, stdout, stderr = ssh.exec_command("sudo echo "ssh key" >> /home/mynewuser/.ssh/authorized_keys")
print('stdout:', stdout.read())
print('stderr:', stderr.read())
ssh.close()
    