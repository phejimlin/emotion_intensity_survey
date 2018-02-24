import json
import decimal
from datetime import datetime
from db import dynamodb
table = dynamodb.Table('user')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if o % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)


def put_user(body):
	survey_id = body['survey_id']
	ptt_account = body['ptt_account']
	

	response = table.put_item(
		Item={
			'survey_id': survey_id,
			'ptt_account': ptt_account
		}
	)

	print("PutItem succeeded:")
	print(json.dumps(response, indent=4, cls=DecimalEncoder))
	return None
