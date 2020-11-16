import boto3
def create_user(user,iam):
    created_user = iam.create_user(
    UserName=user,
    )
    print(created_user)
    response = iam.attach_user_policy(
    UserName = user, #Name of user
    PolicyArn = 'arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
# Policy ARN which you want to asign to user
    )
    print(response)