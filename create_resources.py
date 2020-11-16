import boto3
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
    # Wait for the instance state, default --> one wait is 15 seconds, 40 attempts
    print('Waiting for instance {0} to switch to running state'.format(instance[0].id))
    waiter = ec2.meta.client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance[0].id])
    instance[0].reload()
    print('Instance is running, public IP: {0}'.format(instance[0].public_ip_address))
    instance_id=instance[0].id
    return instance_id, instance[0].public_ip_address
#=============create_and_attach_volume================
def create_and_attach_volume(ec2,device,type,size,instance_id):
    #create
    ssm_client = boto3.client('ssm')
    volume_available_waiter = ec2.get_waiter('volume_available')
    volume_attached_waiter = ec2.get_waiter('volume_in_use')
    try:
        ebs_vol = ec2.create_volume(
        Size=size,
        AvailabilityZone='us-west-1b',
        VolumeType=type
        )
        volume_id =ebs_vol['VolumeId']
        volume_available_waiter.wait(
            VolumeIds=[volume_id]
        )

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
            volume_attached_waiter.wait(
            VolumeIds=[volume_id]
            )
            # use SSM RunCommand to format and mount volume
        
        #pprint(response)
        except Exception as e:
            print('***Error - Failed to attach volume:', volume_id, 'to the instance:', instance_id)
            print(e)
       
        
