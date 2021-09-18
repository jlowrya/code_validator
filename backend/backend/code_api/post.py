import json, random
from backend.verification_code import VerificationCode, SMSCode, EmailCode
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

        return {
            "statusCode": 201,
            "body": body
        }

    return {
        "statusCode": 500,
        "body": "Please provide an email or phone number."
    }