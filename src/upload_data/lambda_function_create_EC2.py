import json
import boto3




ACCESS_KEY = "AKIAJWJKHI6WVWPQKSMA"
SECRET_KEY = "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"
ec2 = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name="eu-west-1")

user_data = """#!/bin/bash
sudo su
yum install python3 -y
yum install git -y
pip3 install --upgrade pip
cd /home/ec2-user
git clone https://github.com/Uranium2/update_cadastre.git
cd update_cadastre
pip install -r requirements.txt 
"""

res = ec2.create_instances(
    ImageId='ami-0ea3405d2d2522162',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    SecurityGroupIds=[
        'sg-0107e6c55125d5988',
    ],
    UserData=user_data,
    
)
instance = ec2.Instance(id=(res[0].id))
instance.wait_until_running()
ec2.create_tags(Resources=[res[0].id], Tags=[{'Key':'name', 'Value':'update_cadastre'}])

# for i in ec2.instances.all():
#     print("Id: {0}\tState: {1}\tLaunched: {2}\tRoot Device Name: {3}".format(i.id, i.state['Name'] ,i.launch_time, i.root_device_name))


