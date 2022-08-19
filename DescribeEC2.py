import json
import boto3


def lambda_handler(event, context):
    ec2=boto3.client('ec2',region_name='us-east-1')
    reservations = ec2.describe_instances(Filters=[
    {
        "Name": "instance-state-name",
        "Values": ["running"],
    }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instances={
            'instance_id' : instance["InstanceId"],
            'instance_type' : instance["InstanceType"],
            'public_ip' : instance["PublicIpAddress"],
            'private_ip' : instance["PrivateIpAddress"]
            }
            print(instances)

    return {
        'statusCode': 200,
        'body': json.dumps(instances)
        }


