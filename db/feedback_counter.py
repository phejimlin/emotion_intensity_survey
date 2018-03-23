import json
import decimal
from datetime import datetime
from db import dynamodb
from botocore.exceptions import ClientError
table = dynamodb.Table('feedback_counter')

class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if o % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)


def update_feedback_counter(body):
	response = table.update_item(
		Key={
			'id': 0
		},
		UpdateExpression="set counter = counter + :p ",
		ExpressionAttributeValues={
			':p': 1
		},
		ReturnValues="UPDATED_NEW"
	)

	print("UpdateItem succeeded:")
	print(json.dumps(response, indent=4, cls=DecimalEncoder))
	return None


def get_feedback_counter():
	try:
		response = table.get_item(
			Key={
				'id': 0,
			}
		)
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		item = response['Item']
		print("GetItem succeeded:")
		return json.dumps(item, indent=4, cls=DecimalEncoder)