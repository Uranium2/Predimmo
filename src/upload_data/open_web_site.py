import os
import boto3
import webbrowser

project_name = 'Predimmo'

ACCESS_KEY = "AKIAINQGD2PLBK42S4NQ"
SECRET_KEY = "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"
ec2 = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name="eu-west-1")

filters = [
    {
        'Name': 'instance-state-name',
        'Values': ['running']
    }
]

instances = ec2.instances.filter(Filters=filters)

RunningInstances = [instance for instance in instances]
print(RunningInstances)
for instance in RunningInstances:
    try:
        if instance.tags[0]['Value'] == project_name:
            dns = instance.public_dns_name
            url = "http://{}:8000/index".format(dns)
            print(url)
            webbrowser.open(url, new=2)
    except:
        print("NO tag")