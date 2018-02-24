import json
from db import survey
from db import user

def user_handler(event, context):
    body = json.loads(event['body'])
    response_body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    print(body)

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {
            "Access-Control-Allow-Origin": "http://emotion-intensity-survey.s3-website-ap-northeast-1.amazonaws.com",
            "Vary": "Origin",
            "Access-Control-Allow-Credentials": True
        },
    }

    if body['survey_id'] is None or body['ptt_account'] is None:
        response_body = {
            "message": "Missing params.",
            "input": event
        }
        response = {
            "statusCode": 400,
            "body": json.dumps(response_body),
            "headers": {
                "Access-Control-Allow-Origin": "http://emotion-intensity-survey.s3-website-ap-northeast-1.amazonaws.com",
                "Vary": "Origin",
                "Access-Control-Allow-Credentials": True
            },
        }
        return response
    else:
        user.put_user(body)
        return response

def survey_handler(event, context):
    body = json.loads(event['body'])
    response_body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {
            "Access-Control-Allow-Origin": "http://emotion-intensity-survey.s3-website-ap-northeast-1.amazonaws.com",
            "Vary": "Origin",
            "Access-Control-Allow-Credentials": True
        },
    }

    print(body)

    if body['survey_id'] is None or body['id'] is None:
        response_body = {
            "message": "Missing params.",
            "input": event
        }
        response = {
            "statusCode": 400,
            "body": json.dumps(response_body),
            "headers": {
                "Access-Control-Allow-Origin": "http://emotion-intensity-survey.s3-website-ap-northeast-1.amazonaws.com",
                "Vary": "Origin",
                "Access-Control-Allow-Credentials": True
            },
        }
        return response
    else:
        survey.put_survey(body)
        return response
