from twilio.rest import Client

account_sid = ""
auth_token = ""
verification = Client(account_sid,auth_token)
twilio_number = "+12025191283"


def sendsms(phone,message):
    verification.messages.create(from_=twilio_number, to=f"+234{phone}",body=message)
