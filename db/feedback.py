import json
import decimal
from datetime import datetime
from db import dynamodb
from botocore.exceptions import ClientError
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
table = dynamodb.Table('feedback')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if o % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)

def put_feedback(body):
	# survey_id = body['survey_id']
	# comment_id = body['id']
	# message = body['message']
	# joy=body.get('joy', 0)
	# angry=body.get('angry', 0)
	# sad=body.get('sad', 0)
	# surprise=body.get('surprise', 0)
	# fear=body.get('fear', 0)

	# response = table.put_item(
	# 	Item={
	# 		'survey_id': survey_id,
	# 		'id': comment_id,
			# 'message': message,
			# 'joy': decimal.Decimal(str(joy)),
			# 'angry': decimal.Decimal(str(angry)),
			# 'sad': decimal.Decimal(str(sad)),
			# 'surprise': decimal.Decimal(str(surprise)),
			# 'fear': decimal.Decimal(str(fear))
	# 	}
	# )

	survey_id = body['survey_id']
	feedback_id = body['feedback_id']

	# To fix "Float types are not supported. Use Decimal types instead"
	data_list = body['data']
	json_data_list = json.dumps(data_list)

	# for data in data_list:
	# 	json_data_list.append(json.dumps(data))
	# 	data['joy'] = decimal.Decimal(str(data['joy'])),
	# 	data['angry'] = decimal.Decimal(str(data['angry'])),
	# 	data['sad'] = decimal.Decimal(str(data['sad'])),
	# 	data['surprise'] = decimal.Decimal(str(data['surprise'])),
	# 	data['fear'] = decimal.Decimal(str(data['fear']))
	
	# print(json_data_list)
	response = table.put_item(
		Item={
			"id": feedback_id,
			'survey_id': survey_id,
			"data": json_data_list
		}
	)

	print("put_feedback succeeded:")
	# print(json.dumps(response, indent=4, cls=DecimalEncoder))
	return None


def update_feedback(body):
	feedback_id = body['feedback_id']
	ptt_account = body['ptt_account']

	table.update_item(
		Key={
			'id': feedback_id
		},
		UpdateExpression="set ptt_account=:p",
		ExpressionAttributeValues={
			':p': ptt_account
		},
		ReturnValues="UPDATED_NEW"
	)

	print("update ptt_account succeeded:")
	# print(json.dumps(response, indent=4, cls=DecimalEncoder))
	return None

def check_count_of_feedback(survey_id):
	try:
		response = table.query(
			IndexName='survey_id-index-copy',
			KeyConditionExpression=Key('survey_id').eq(survey_id)
		)
	except ClientError as e:
		print("check_count_of_feedback Error")
		print(e.response['Error']['Message'])
	else:
		items = response['Items']
		print("check_count_of_feedback succeeded:")
		length_of_feedback = len(items)
		print(length_of_feedback)
		if length_of_feedback >= 3:
			return True
		else:
			return False
