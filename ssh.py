import paramiko
import time
def ssh_connect_with_retry(ssh, ip_address, retries,user,pemfile):
    if retries > 3:
        return False
    # privkey = paramiko.RSAKey.from_private_key_file(
    #   'new-keypair.pem')
    privkey = paramiko.RSAKey.from_private_key_file(
      pemfile)
    interval = 5
    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        ssh.connect(hostname=ip_address,
                    username=user, pkey=privkey)
        stdin, stdout, stderr = ssh.exec_command("sudo mkfs -t ext4 /dev/xvdf;sudo mkdir /data;sudo mount /dev/xvdf /data;sudo adduser user1;sudo adduser user2")
        print('stdout:', stdout.read())
        print('stderr:', stderr.read())
        print("added users")
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)
