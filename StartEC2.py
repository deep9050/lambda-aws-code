import json
import boto3

def lambda_handler(event, context):
        ec2=boto3.client('ec2',region_name='us-east-1')
        instances= ec2.start_instances(InstanceIds=['i-05d12af2c23c658d7'])
        print(instances)
        return {
                'statusCode': 200,
                'body': json.dumps(instances)
            }