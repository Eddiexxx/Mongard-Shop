from kavenegar import *



def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('4E425268704F336A472F6B394E4D566D333661654B334638397231414134755541484D7279446E6A786A593D')
        params = {'sender': '2000500666',
                  'receptor': phone_number,
                  'message': f' کد تایید شما {code} '
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)

