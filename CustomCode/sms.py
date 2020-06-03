from twilio.rest import Client
# account_sid = "AC7227807a67f5af6f2ca7c66595c1ca6f"
# auth_token = "a30830b7c5f8b7be61677882c17141f9"

account_sid = "AC40357f41c91c5e5be43cbd62a609c78d"
auth_token = "82775d57d24cd794867d96696d245d50"
verification = Client(account_sid,auth_token)
twilio_number = "+12025191283"




verification.messages.create(
                    from_=twilio_number, 
                    to="+2348130103966",
                    body='You verification code is: 1234567(This is a test)'                
                    )