import json
import boto3




ACCESS_KEY = "AKIAINQGD2PLBK42S4NQ"
SECRET_KEY = "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"
ec2 = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name="eu-west-1")

tags = ["django_deploy"]
instances = []

for tag in tags:
    user_data = """Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
sudo su
yum install python3 -y
yum install git -y
pip3 install --upgrade pip
cd /home/ec2-user
#git clone https://github.com/Uranium2/{}.git
#chmod -R ugo+rwx {}
#cd {}
#git pull
echo -e "{}\n{}\n{}\n{}\n{}" > aws_keys
#pip install -r requirements.txt
#python3 stop_instance.py
    """.format(tag, tag, tag, ACCESS_KEY, SECRET_KEY, "predimodbinstance.cbiog1ld7y5x.eu-west-1.rds.amazonaws.com",
    "admin", "N8XR3u#m9[5Mk6UK", "3306")

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
    instances.append((instance, res))

for i, instance in enumerate(instances):
    instance[0].wait_until_running()
    ec2.create_tags(Resources=[instance[1][0].id], Tags=[{'Key':'name', 'Value': tags[i]}])
