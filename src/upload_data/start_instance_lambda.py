import os
import boto3

def lambda_handler(event, context):
    filters = [
        {
            'Name': 'instance-state-name',
            'Values': ['stopped']
        }
    ]
    
    ACCESS_KEY = "AKIAINQGD2PLBK42S4NQ"
    SECRET_KEY = "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"
    
    ec2 = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name="eu-west-1")
   
    instances = ec2.instances.filter(Filters=filters)
    
    StoppedInstances = [instance for instance in instances]
    
    ec2_instance = event.get('ec2_instance')
    
    for instance in StoppedInstances:
        print(instance.tags[0]['Value'])
        if instance.tags[0]['Value'] == ec2_instance:
            print(instance.id)
            instance.start()