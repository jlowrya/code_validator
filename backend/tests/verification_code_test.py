import pytest, os
from backend import verification_code
from backend.resources import table

TEST_CODE = 'abc'

for code_type in [
    verification_code.VerificationCode, 
    verification_code.EmailCode, 
    verification_code.SMSCode]:

    code = code_type(TEST_CODE)

    assert code.code == TEST_CODE

    for comm_type in verification_code.CommType:
        code.save(comm_type, 'test')
        item = table.get_item(
                TableName=os.getenv('TABLENAME'),
                Key={
                    'pk': {
                        'S': f'{comm_type.value}#test',
                    }
                }
            )['item']
        assert item['code']['S'] == TEST_CODE

    if(code_type==verification_code.VerificationCode):
        with pytest.raises:
            code.send()
    else:
        code.send()
