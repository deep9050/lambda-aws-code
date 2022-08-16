import json
import boto3
ssm_client = boto3.client('ssm', region_name='us-east-1')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
      
    try:
        params={"commands":["systemctl restart nginx"],"workingDirectory":["/root"],"executionTimeout":["3600"]}
        response = ssm_client.send_command(DocumentName="AWS-RunShellScript", Targets=[{"Key":"tag:Name","Values":["EC2-1"]}],Comment='logging the', TimeoutSeconds=600, Parameters=params)
        sns_client.publish(
                TopicArn ='arn:aws:sns:us-east-1:209586379301:Cron-job-Status',
                Subject = 'Last Successfully update ',
                Message = 'Server : '+'Run successfully nginx server\n'+'instanceId :'+'i-0c9e1c00f46ef508c\n'
            
            )

        return {
                    'statusCode': 200,
                    'body': json.dumps('Successfully Run nginx Server instanceId=i-0c9e1c00f46ef508c')
                }
        
    except Exception as e:
        sns_client.publish(
        TopicArn ='arn:aws:sns:us-east-1:209586379301:Cron-job-Status',
        Subject = 'Last Failed Ngnix Server',
        Message= 'Server : '+'Server failed\n'+'error : '+f'{e}\n'+'instanceId : '+'i-0c9e1c00f46ef508c\n'
    
            )
        return {
                'statusCode': 400,
                'body': e
            }
                    
        