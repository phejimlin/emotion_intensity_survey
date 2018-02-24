import boto3


session = boto3.Session()
credentials = session.get_credentials()

# Initialize dynamodb
dynamodb = boto3.resource('dynamodb',region_name='ap-northeast-1')
