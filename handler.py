import json
from db import survey
from db import feedback_counter
from db import feedback

# "http://emotion-intensity-survey.s3-website-ap-northeast-1.amazonaws.com"
def feedback_update_handler(event, context):
    body = json.loads(event['body'])
    response_body = {
        "message": "success",
        "input": event
    }

    print(body)

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Vary": "Origin",
            "Access-Control-Allow-Credentials": True
        },
    }

    if body['feedback_id'] is None or body['ptt_account'] is None:
        response_body = {
            "message": "Missing params.",
            "input": event
        }
        response = {
            "statusCode": 400,
            "body": json.dumps(response_body),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Vary": "Origin",
                "Access-Control-Allow-Credentials": True
            },
        }
        return response
    else:
        feedback.update_feedback(body)
        return response

def survey_handler(event, context):
    # data = survey.get_survey(0)
    data = survey.choise_survey()
    response = {
        "statusCode": 200,
        "body": data,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Vary": "Origin",
            "Access-Control-Allow-Credentials": True
        },
    }

    # TODO survey_id 先直接autoincreatment  240以上後 再判斷還沒完成三筆的survey list 回傳給user
    # if survey_list 是空的之後 回傳Null survey結束
    # feedback_counter.update_feedback_counter()
    return response

def feedback_handler(event, context):
    body = json.loads(event['body'])
    response_body = {
        "message": "success",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Vary": "Origin",
            "Access-Control-Allow-Credentials": True
        },
    }

    # print(body)

    if body['survey_id'] is None or body['feedback_id'] is None or body['data'] is None:
        response_body = {
            "message": "Missing params.",
            "input": event
        }
        response = {
            "statusCode": 400,
            "body": json.dumps(response_body),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Vary": "Origin",
                "Access-Control-Allow-Credentials": True
            },
        }
        return response
    else:
        data_list = body['data']
        if data_list[-1]['label'] != 'joy':
            response_body = {
                "message": "Invalid feedback!",
                "input": event
            }
            response = {
                "statusCode": 400,
                "body": json.dumps(response_body),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Vary": "Origin",
                    "Access-Control-Allow-Credentials": True
                },
            }
            return response
        else:
            feedback.put_feedback(body)
            survey_id = body['survey_id']
            if feedback.check_count_of_feedback(survey_id):
                # feedback count is greater than 3
                survey.update_survey_finished(survey_id)
            return response