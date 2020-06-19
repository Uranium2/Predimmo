import json
import boto3




ACCESS_KEY = "AKIAJI26MDZ6Q5KV2NYA"
SECRET_KEY = "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"
ec2 = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name="eu-west-1")

tags = ["Predimmo"]
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
yum update -y
yum install python3 -y
yum install git -y
pip3 install --upgrade pip
cd /home/ec2-user
git clone https://FlorianBergeron:wPG4b.rh@github.com/Uranium2/{}.git
chmod -R 777 {}
cd {} 
DIR="/home/ec2-user/{}/.venv/"
if [ -d "$DIR" ]; then
    echo "Directory already exist"
else
    python3 -m venv .venv
fi
source .venv/bin/activate
git stash
git pull
echo -e "{}\n{}\n{}\n{}\n{}" > aws_keys
curl ifconfig.me > my_ip
curl -s http://169.254.169.254/latest/meta-data/public-hostname > dns
IP=$(<my_ip)
DNS=$(<dns)
sed -i -e "s/\[\]/\['$IP','$DNS'\]/g" src/web/django/projet_annuel/settings.py
pip3 install -r requirements.txt
python3 src/web/django/manage.py runserver 0.0.0.0:8000
    """.format(tag, tag, tag, tag, ACCESS_KEY, SECRET_KEY, "predimodbinstance.cbiog1ld7y5x.eu-west-1.rds.amazonaws.com",
    "admin", "N8XR3u#m9[5Mk6UK", "3306")

# AWS Linux 2: ami-0ea3405d2d2522162
# RedHat: ami-08f4717d06813bf00
# Ubuntu 18: ami-0701e7be9b2a77600

# SG (SSH): sg-0107e6c55125d5988
# SG (SSH + HTTP): sg-02e589e6e992b3f07

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
