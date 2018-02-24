import json
import decimal
from datetime import datetime
from db import dynamodb
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


def put_survey(body):
	survey_id = body['survey_id']
	comment_id = body['id']
	content = body['content']
	joy=body.get('joy', 0)
	angry=body.get('angry', 0)
	sad=body.get('sad', 0)
	surprise=body.get('surprise', 0)
	fear=body.get('fear', 0)

	response = table.put_item(
		Item={
			'survey_id': survey_id,
			'id': comment_id,
			'content': content,
			'joy': decimal.Decimal(str(joy)),
			'angry': decimal.Decimal(str(angry)),
			'sad': decimal.Decimal(str(sad)),
			'surprise': decimal.Decimal(str(surprise)),
			'fear': decimal.Decimal(str(fear))
		}
	)

	print("PutItem succeeded:")
	print(json.dumps(response, indent=4, cls=DecimalEncoder))
	return None
