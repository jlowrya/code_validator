from backend.verification_code import VerificationCode, SMSCode, EmailCode

def get(event, context):
    query_params = event.get('queryStringParameters')

    code = query_params.get('code')
    phone = query_params.get('phone')

    #if successful return 200 code
    if(SMSCode(code=code, phone=phone).verify()):
        return {
            "headers": {'Access-Control-Allow-Origin': '*'},
            "statusCode": 200,
            "body": "Code successfully validated"
        }
    else:
        return {
            "headers": {'Access-Control-Allow-Origin': '*'},
            "statusCode": 404,
            "body": "Code incorrect"
        }