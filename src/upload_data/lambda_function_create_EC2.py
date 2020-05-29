import json
import boto3




ACCESS_KEY = "AKIAJWJKHI6WVWPQKSMA"
SECRET_KEY = "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"
ec2 = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name="eu-west-1")

res = ec2.create_instances(
    ImageId='ami-0ea3405d2d2522162',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    SecurityGroupIds=[
        'sg-0107e6c55125d5988',
    ],
)
instance = ec2.Instance(id=(res[0].id))
instance.wait_until_running()


# To terminate : run in EC2
# ec2.instances.filter(InstanceIds = [res[0].id]).terminate()
    

