import json
import boto3

def lambda_handler(event, context):
    ec2=boto3.client('ec2',region_name='us-east-1')
    instances= ec2.terminate_instances(InstanceIds=['i-06dc98b9948c74729'])
    print(instances)
    return {
            'statusCode': 200,
            'body': json.dumps(instances)
    }