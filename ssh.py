import paramiko
import time
def ssh_connect_with_retry(ssh, ip_address, retries,user):
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
      'new-keypair.pem')
    interval = 5
    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        ssh.connect(hostname=ip_address,
                    username=user, pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)
# import boto3
# iam = boto3.client('iam')

# for user in iam.list_users()['Users']:
#  print("User: {0}\nUserID: {1}\nARN: {2}\nCreatedOn: {3}\n".format(
#  user['UserName'],
#  user['UserId'],
#  user['Arn'],
#  user['CreateDate']
#  )
#  )