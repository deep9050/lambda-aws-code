import json
import base64
import boto3


def lambda_handler(event, context):
    s3 = boto3.client("s3")
    print(s3)
    # retrieving data from event
    get_file_content = event["body"]
    print(get_file_content)

    # decoding data
    decode_content = base64.b64decode(get_file_content)
    print(decode_content)
    

    # uploading file to S3 bucket
    s3_upload = s3.put_object(Bucket="api-s3-gateway", Key="file.pdf", Body=decode_content)

    return {"statusCode": 200, "body": json.dumps("Thanks for using!")}