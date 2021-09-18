import os
if(os.getenv('STAGE', 'local')!='local'):
    import boto3
else:
    import localstack_client.session as boto3


table = boto3.client('dynamodb')

sns = boto3.client('sns')

ses = boto3.client('ses')





