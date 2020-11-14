import yaml
import boto3
filename='new-keypair.pem'
a_yaml_file = open("config.yaml")
values = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
InstanceType=values['server']['instance_type']
ImageId=values['server']['ami_type']
MinCount=values['server']['min_count']
MaxCount=values['server']['max_count']
KeyName=values['server']['KeyName']
n=len(values['server']['volumes'])
for i in range(n):
    x=values['server']['volumes'][i]
    # li=list(x.values())
    # print(li)
    device=x['device']
    size=x['size_gb']
    ty=x['type']
    mount=x['mount']
    print(device,size,ty,mount)