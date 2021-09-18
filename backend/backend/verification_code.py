
from abc import abstractmethod
from backend.resources import table, sns, ses

import random, os
import enum


class CommType(enum.Enum):
    SMS = 'SMS'
    EMAIL = 'EMAIL'


class VerificationCode:
    def __init__(self, code : str, comm_type: CommType):
        self.code = code
        self.comm_type = comm_type

    def save(self, info : str) -> bool:
        try:
            table.put_item(
                TableName=os.getenv('TABLENAME'),
                Item={
                    'pk': {
                        'S': f'{self.comm_type.value}#{info}'
                    },
                    'code': {
                        'S': self.code
                    }

                },
                ReturnConsumedCapacity='TOTAL'
            )
            return True
        except Exception as e:
            print(e)
            return False

    def save_and_send(self) -> None:
        self.save()
        self.send()
    
    def verify(self, info : str):
        response = table.query(
            TableName=os.getenv('TABLENAME'),
            ReturnConsumedCapacity='TOTAL',
            FilterExpression='code = :code',
            KeyConditionExpression='pk = :pk',
            ExpressionAttributeValues={
                ':code': {
                    'S': f'{self.code}',
                },
                ':pk': {
                    'S': f'{self.comm_type.value}#{info}'
                }
            }
        )
        return len(response['Items'])>0


    #should return random integer as a string
    @classmethod
    def gen_code(cls, num_digits : int = 6) -> str:
        return str(random.randint(10**(num_digits-1), 10**num_digits)) 

    @abstractmethod
    def send(self) -> bool:
        pass

# class EmailCode(VerificationCode):
#     def __init__(self, email: str):
#         self.email = email
#         self.comm_type = CommType.EMAIL
    
#     def save(self):
#         super.save(self.comm_type, self.email)

#     def send(self):
#         try:
#             ses.send_email(
#                 #TODO: verify email address for source to use
#                 Source='string',
#                 Destination={
#                     'ToAddresses': [
#                         self.email,
#                     ]
#                 },
#                 Message={
#                     'Subject': {
#                         'Data': 'Validation code',
#                         #IDEA: UTF supports emojis, so could potentially allow for verification via emojis
#                         'Charset': 'UTF-8'
#                     },
#                     'Body': {
#                         'Text': {
#                             'Data': self.code,
#                             'Charset': 'UTF-8'
#                         }
#                     }
#                 }
#             )
#             return True
#         except Exception:
#             return False

class SMSCode(VerificationCode):
    def __init__(self, phone, **kwargs):
        self.phone = phone 
        kwargs["comm_type"]=CommType.SMS
        super().__init__(**kwargs)
        
    def verify(self):
        return super().verify(self.phone)

    def save(self):
        super().save(self.phone)
        

    def send(self):
        if(os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_AUTH_TOKEN')):
            from twilio.rest import Client
            client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
            client.api.account.messages.create(
                    to=self.phone,
                    from_="+17604073113",
                    body=f'{self.code}'
            )
        else:
            sns.publish(
                PhoneNumber=self.phone,
                Message=f'{self.code}',
                Subject='Verification code',
            )


