import json, random
from backend.verification_code import VerificationCode, SMSCode, EmailCode
from requests import Response, status_codes
###
# primary key = {email} or {phone}
# attributes - ttl, code
#   
###
def post(event, context):
    #receive phone number
    query_params = event.get('queryStringParameters')

    email = query_params.get('email', None)
    phone = query_params.get('phone', None)

    code = VerificationCode.gen_code()

    if email or phone:
        body = "Verification code sent to "

        if (phone):
            SMSCode(code=code, phone=phone).save_and_send()
            body += f"{phone}"

        return Response(
            headers={'Access-Control-Allow-Origin': '*'},
            status_code=201,
            body=body
        ).json()

    return Response(status_code=500,body="Please provide an email or phone number.").json()

def get(event, context):
    query_params = event.get('queryStringParameters')

    code = query_params.get('code')
    phone = query_params.get('code')

    #if successful return 200 code
    if(SMSCode(code=code, phone=phone).verify()):
        return {
            "statusCode": 200,
            "body": "Code successfully validated"
        }
    else:
        return {
            "statusCode": 404,
            "body": "Code incorrect"
        }