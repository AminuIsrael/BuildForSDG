import re


#Email Validator
re_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
def checkmail(email):  
    if(re.search(re_email,email)):
        return True 
    else:  
        return False


re_phone = r'((^090)([123589]))|((^070)([1-9]))|((^080)([1-9]))|((^081)([0-9]))(\d{7})'
def checkphone(phone_number):
    if(re.search(re_phone, phone_number)):
        return True
    else:  
        return False