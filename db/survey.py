import json
import decimal
from datetime import datetime
from db import dynamodb
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import random
table = dynamodb.Table('survey')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if o % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)

def choise_survey():
	# 找還沒完成三筆的survey 回傳給user
	fe = Key('collected_feedback').eq(False)
	# pe = "#yr, title, info.rating"
	# Expression Attribute Names for Projection Expression only.
	response = table.scan(
		FilterExpression=fe
	)
	length = len(response['Items'])
	if length > 0:
		random_seed = random.randint(0, length - 1)
		print(random_seed)
		return json.dumps(response['Items'][random_seed], cls=DecimalEncoder)
	else:
		return json.dumps({"data": None})

def get_survey(id):
	try:
		response = table.get_item(
			Key={
				'id': id,
			}
		)
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		item = response['Item']
		print("GetItem succeeded:")
		return json.dumps(item, indent=4, cls=DecimalEncoder)

def update_survey_finished(id):
	response = table.update_item(
		Key={
			'id': id
		},
		UpdateExpression="set collected_feedback=:p",
		ExpressionAttributeValues={
			':p': True
		},
		ReturnValues="UPDATED_NEW"
	)

	print("UpdateItem succeeded:")
	print(json.dumps(response, indent=4, cls=DecimalEncoder))
	return None