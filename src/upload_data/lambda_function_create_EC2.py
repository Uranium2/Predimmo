import json
import boto3




ACCESS_KEY = "AKIAIV76PKAW63PGPERA"
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


# Se connecter à l'instance EC2 en SSH. Peut etre rajouter la clé SSH (chemin de la clé) dans create_instances (fichier.pem)

# Reussir a trouver un moyen de lancer du code via SSH
    # Dans le code qui va etre executé en SSH, il va DL le fichier python ou script (Installation Python3)


# ES => EC2 (python => Model/training) => ES

# To terminate : run in EC2
# ec2.instances.filter(InstanceIds = [res[0].id]).terminate()
    

