import json
import boto3

def lambda_handler(event, context):
        ec2=boto3.client('ec2',region_name='us-east-1')
        instances=ec2.run_instances(
            ImageId="ami-052efd3df9dad4825",
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName="vikas"
        )
        instances={'instances':instances["Instances"][0]["InstanceId"]}

        print(instances)