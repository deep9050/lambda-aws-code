import json
import boto3
import time
from datetime import datetime

# given datetime
current_date = datetime.now()
ssm_client = boto3.client('ssm', region_name='us-east-1')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
      
    try:
        now=datetime.now()
        params={"commands":["systemctl restart nginx"],"workingDirectory":["/root"],"executionTimeout":["3600"]}
        response = ssm_client.send_command(DocumentName="AWS-RunShellScript", Targets=[{"Key":"tag:Name","Values":["EC2-1"]}],Comment='logging the', TimeoutSeconds=600, Parameters=params)
                
                #Sleep lambda 200 ms lambda
        time.sleep(0.2)
                       
                        #Get a list commend to check a status 
        list_item2=ssm_client.list_commands(CommandId=response['Command']['CommandId'])
        later=datetime.now()
        
        #When status is pending Or InProgress then start loop and sleep lambda one second after that to check status when condition are follow
        
        while list_item2['Commands'][0]['Status'] == 'Pending' or list_item2['Commands'][0]['Status'] == 'InProgress':
            time.sleep(1)
            list_item2=ssm_client.list_commands(CommandId=response['Command']['CommandId'])
            later=datetime.now()
            if int((later - now).total_seconds()) >= 650:
                break
            
            #when status are success then send Email 
        if list_item2['Commands'][0]['StatusDetails'] == 'Success' and list_item2['Commands'][0]['Status'] == 'Success':
            
            #Get a list command invocation to find a instanceId by commandId
            list_item=ssm_client.list_command_invocations(CommandId=response['Command']['CommandId']) 
            
            #Get a commend invocation to find output and error in a command by a instanceId and CommandId
            list2=ssm_client.get_command_invocation(CommandId=response['Command']['CommandId'],InstanceId=list_item['CommandInvocations'][0]['InstanceId'])
            inst=list2['InstanceId']
            er=list2['StandardOutputContent']
            sns_client.publish(
                    TopicArn ='arn:aws:sns:us-east-1:209586379301:Cron-job-Status',
                    Subject = 'Last Cron-Job got Success',
                    Message= 'Message : '+'Last CronJob Success\n'+'status : '+'Success\n'+'StatusDetails : '+ 'Success\n'+'InstanceId : '+ f'{inst}\n'+'Output : '+ f'{er}\n'
                    )
            return {
                    'statusCode': 200,
                    'body': json.dumps('Successfully Run nginx Server instanceId=i-0c9e1c00f46ef508c')
                }
                
        elif list_item2['Commands'][0]['Status'] == 'Success' and list_item2['Commands'][0]['StatusDetails'] != 'Success':
            sd=list_item2['Commands'][0]['StatusDetails']
            sns_client.publish(
                    TopicArn ='arn:aws:sns:us-east-1:209586379301:Cron-job-Status',
                    Subject = 'Last Cron-Job got something missing',
                    Message= 'Message : '+'Last CronJob something missing\n'+'status : '+'Success\n'+'StatusDetails : '+ f'{sd}\n'
                    )
            return {
                    'statusCode': 404,
                    'body': json.dumps('Not found')
                    }
                    
        elif list_item2['Commands'][0]['Status'] == 'Failed' and list_item2['Commands'][0]['StatusDetails'] == 'Failed':
            list_item=ssm_client.list_command_invocations(CommandId=response['Command']['CommandId'])
            list2=ssm_client.get_command_invocation(CommandId=response['Command']['CommandId'],InstanceId=list_item['CommandInvocations'][0]['InstanceId'])
            
            print(list2)
            inst=list2['InstanceId']
            er=list2['StandardErrorContent']
            sns_client.publish(
                    TopicArn ='arn:aws:sns:us-east-1:209586379301:Cron-job-Status',
                    Subject = 'Last Cron-Job got Failed',
                    Message= 'Message : '+'Failed Last CronJob\n'+'status : '+'Failed\n'+'StatusDetails : '+ 'Failed\n'+'InstanceId : '+ f'{inst}\n'+'error : '+ f'{er}\n'
                    )
            return {
                
                    'statusCode': 408,
                    'body': json.dumps('failed command')
                    }
                    
            
        else:
            sns_client.publish(
                    TopicArn ='arn:aws:sns:us-east-1:209586379301:Cron-job-Status',
                    Subject = 'Timeout Last Cron-Job',
                    Message= 'Message : '+'Failed CronJob\n'+'error : '+'Timeout Cron job\n'
                )
            return {
                
                    'statusCode': 408,
                    'body': json.dumps('timeout')
                
                    }
      
    except Exception as e:
        sns_client.publish(
        TopicArn ='arn:aws:sns:us-east-1:209586379301:Cron-job-Status',
        Subject = ' Last Cron-Job got Something wrong',
        Message= 'Message : '+'Something wrong in a Cron-job\n'+'error : '+f'{e}\n'
            )
        raise e