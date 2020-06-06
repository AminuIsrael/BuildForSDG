import re


#Email Validator
re_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
def checkmail(email):  
    if(re.search(re_email,email)):
        return True 
    else:  
        return False


re_phone = '^(-?\d+\.\d+)'
def checkphone(phone_number):
    if(re.search(phone_number,re_phone)):
        return True 
    else:  
        return False
    

print(checkphone('08130103966'))