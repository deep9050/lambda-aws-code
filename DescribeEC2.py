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



{'CommandInvocations': [
    {'CommandId': 'e5e921ca-f0dd-4cf6-b48b-e4ed75a4ff4e', 'InstanceId': 'i-0c9e1c00f46ef508c', 'InstanceName': 'ip-172-31-84-150.ec2.internal', 'Comment': 'logging the', 'DocumentName': 'AWS-RunShellScript', 'DocumentVersion': '$DEFAULT', 'RequestedDateTime': datetime.datetime(2022, 8, 18, 13, 0, 51, 912000, tzinfo=tzlocal()), 'Status': 'Success', 'StatusDetails': 'Success', 'StandardOutputUrl': '', 'StandardErrorUrl': '', 'CommandPlugins': [], 'ServiceRole': '', 'NotificationConfig': {'NotificationArn': '', 'NotificationEvents': [], 'NotificationType': ''}, 'CloudWatchOutputConfig': {'CloudWatchLogGroupName': '', 'CloudWatchOutputEnabled': False}},

 {'CommandId': 'e5e921ca-f0dd-4cf6-b48b-e4ed75a4ff4e', 'InstanceId': 'i-0657b400c39cbbd64', 'InstanceName': 'ip-172-31-88-210.ec2.internal', 'Comment': 'logging the', 'DocumentName': 'AWS-RunShellScript', 'DocumentVersion': '$DEFAULT', 'RequestedDateTime': datetime.datetime(2022, 8, 18, 13, 0, 51, 766000, tzinfo=tzlocal()), 'Status': 'Failed', 'StatusDetails': 'Failed', 'StandardOutputUrl': '', 'StandardErrorUrl': '', 'CommandPlugins': [], 'ServiceRole': '', 'NotificationConfig': {'NotificationArn': '', 'NotificationEvents': [], 'NotificationType': ''}, 'CloudWatchOutputConfig': {'CloudWatchLogGroupName': '', 'CloudWatchOutputEnabled': False}}
 
 ],


 'ResponseMetadata': {'RequestId': '797895df-2c70-48ab-a035-fb43313f0291', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 18 Aug 2022 13:00:52 GMT', 'content-type': 'application/x-amz-json-1.1', 'content-length': '1152', 'connection': 'keep-alive', 'x-amzn-requestid': '797895df-2c70-48ab-a035-fb43313f0291'}, 'RetryAttempts': 0}}
