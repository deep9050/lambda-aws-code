import json
import os
import boto3
import time
from datetime import datetime
TopicArn= os.getenv('TopicArn')
ssm_client = boto3.client('ssm', region_name='us-east-1')
sns_client = boto3.client('sns')

def lambda_handler(event, context):
      
    try:
        now=datetime.now()
        params={"commands":["systemctl restart nginx"],"workingDirectory":["/root"],"executionTimeout":["3600"]}
        response = ssm_client.send_command(DocumentName="AWS-RunShellScript", Targets=[{"Key":"tag:Nginx-DeployEnv","Values":["prod"]}],Comment='logging the', TimeoutSeconds=600, Parameters=params)
                
                #Sleep lambda 200 ms lambda
        time.sleep(1)
                       
                        #Get a list commend to check a status 
        list_item2=ssm_client.list_commands(CommandId=response['Command']['CommandId'])
        later=datetime.now()
        
        #Sleep lambda for one second when status in pending or Inprogress
        while list_item2['Commands'][0]['Status'] == 'Pending' or list_item2['Commands'][0]['Status'] == 'InProgress':
            time.sleep(1)
            list_item2=ssm_client.list_commands(CommandId=response['Command']['CommandId'])
            later=datetime.now()
            if int((later - now).total_seconds()) >= 650:
                break
            
            
            #when status is  success then  send  Email 
            
        print(list_item2)
        if list_item2['Commands'][0]['StatusDetails'] == 'Success' and list_item2['Commands'][0]['Status'] == 'Success':
            
            #Get a list command invocation to find a instanceId by commandId
            list_item=ssm_client.list_command_invocations(CommandId=response['Command']['CommandId'])
            TC=list_item2['Commands'][0]['TargetCount']
            EC=list_item2['Commands'][0]['ErrorCount']
            CC=list_item2['Commands'][0]['CompletedCount']
            CI=response['Command']['CommandId']
            
            message='Message : '+'Last CronJob Success\n'+'CommandId : '+f'{CI}\n' +'ErrorCount : '+f'{EC}\n'+'TargetCount : '+ f'{TC}\n'+'CompletedCount : '+f'{CC}\n'
            
            for i in range(1,len(list_item['CommandInvocations'])+1):
                list2=ssm_client.get_command_invocation(CommandId=response['Command']['CommandId'],InstanceId=list_item['CommandInvocations'][i-1]['InstanceId'])
                inst=list2['InstanceId']
                Op=list2['StandardOutputContent']
                st=list2['Status']
                sd=list2['StatusDetails']
                message=message+'\n\ntarget  :  '+f'{i}\n'+'Status : '+f'{st}\n'+'StatusDetails : '+ f'{sd}\n'+'InstanceId : '+ f'{inst}\n'+'Output : '+ f'{Op}\n'
            
            sns_client.publish(
                    TopicArn =os.getenv('TopicArn'),
                    Subject = 'Last Cron-Job got Success',
                    Message=message
                     )
            return {
                    'statusCode': 200,
                    'body': json.dumps('Successfully completed nginx restart')
                }
                
        elif list_item2['Commands'][0]['Status'] == 'Success' and list_item2['Commands'][0]['StatusDetails'] != 'Success':
            sd=list_item2['Commands'][0]['StatusDetails']
            sns_client.publish(
                    TopicArn =os.getenv('TopicArn'),
                    Subject = 'Last Cron-Job got something missing',
                    Message= 'Message : '+'Last CronJob something missing\n'+'status : '+'Success\n'+'StatusDetails : '+ f'{sd}\n'
                    )
            return {
                    'statusCode': 404,
                    'body': json.dumps('Not found')
                    }
                    
        elif list_item2['Commands'][0]['Status'] == 'Failed' and list_item2['Commands'][0]['StatusDetails'] == 'Failed':
            list_item=ssm_client.list_command_invocations(CommandId=response['Command']['CommandId'])
            TC=list_item2['Commands'][0]['TargetCount']
            EC=list_item2['Commands'][0]['ErrorCount']
            CC=list_item2['Commands'][0]['CompletedCount']
            CI=response['Command']['CommandId']
            
            print(len(list_item['CommandInvocations']),'to check length')
            message='Message : '+'Failed Last CronJob\n'+'CommandId : '+f'{CI}\n' +'ErrorCount : '+f'{EC}\n'+'TargetCount : '+ f'{TC}\n'+'CompletedCount : '+f'{CC}\n'
            
            for i in range(1,len(list_item['CommandInvocations'])+1):
                list2=ssm_client.get_command_invocation(CommandId=response['Command']['CommandId'],InstanceId=list_item['CommandInvocations'][i-1]['InstanceId'])
                inst=list2['InstanceId']
                er=list2['StandardErrorContent']
                st=list2['Status']
                sd=list2['StatusDetails']
                message=message+'\n\ntarget  :  '+f'{i}\n'+'Status : '+f'{st}\n'+'StatusDetails : '+ f'{sd}\n'+'InstanceId : '+ f'{inst}\n'+'error : '+ f'{er}\n'
            
             
            sns_client.publish(
                    TopicArn =os.getenv('TopicArn'),
                    Subject = 'Last Cron-Job got Failed',
                    Message=message
                    )
            return {
                
                    'statusCode': 408,
                    'body': json.dumps('failed command')
                    }
                    
            
        else:
            sns_client.publish(
                    TopicArn =os.getenv('TopicArn'),
                    Subject = 'Timeout Last Cron-Job',
                    Message= 'Message : '+'Failed CronJob\n'+'error : '+'Timeout Cron job\n'
                )
            return {
                
                    'statusCode': 408,
                    'body': json.dumps('timeout')
                
                    }
      
    except Exception as e:
        sns_client.publish(
        TopicArn = os.getenv('TopicArn'),
        Subject = ' Last Cron-Job got Something wrong',
        Message= 'Message : '+'Something wrong in a Cron-job\n'+'error : '+f'{e}\n'
            )
        raise e