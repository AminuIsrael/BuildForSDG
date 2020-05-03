from datetime import datetime,timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from api.models import User,otp
from CustomCode import string_generator,password_functions,validator,autentication
from django.http import HttpResponse #httpresponse
from django.core.mail import send_mail #django email module
from django.conf import settings

# Create your views here.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error" : "0",
        "message" : "Successful",
    }
    return Response(return_data)

@api_view(["POST"])
def user_registration(request):
    try:
        firstName = request.data.get('firstname',None)
        lastName = request.data.get('lastname',None)
        phoneNumber = request.data.get('phonenumber',None)
        email = request.data.get('email',None)
        gender = request.data.get('gender',None)
        password = request.data.get('password',None)
        address = request.data.get('address',None)
        lga = request.data.get('lga',None)
        state = request.data.get('state',None)
        country = request.data.get('country',None)
        reg_field = [firstName,lastName,phoneNumber,email,password,address,lga,state,country]
        if not None in reg_field and not "" in reg_field:
            if User.objects.filter(user_phone =phoneNumber).exists() or User.objects.filter(email =email).exists():
                return_data = {
                    "error": "1",
                    "message": "User Exists"
                }
            else:
                #generate user_id
                userRandomId = string_generator.alphanumeric(20)
                #encrypt password
                encryped_password = password_functions.generate_password_hash(password)
                #Save user_data
                new_userData = User(user_id=userRandomId,firstname=firstName,lastname=lastName,
                                email=email,user_phone=phoneNumber,user_gender=gender,
                                user_password=encryped_password,user_address=address,
                                user_state=state,user_LGA=lga,user_country=country)
                new_userData.save()
                #Generate OTP
                code = string_generator.numeric(6)
                #Save OTP
                user_OTP =otp(user=new_userData,otp_code=code)
                user_OTP.save()

                #EMAIL CONDITION, CHECK IF SAVE IS SUCCESSFUL
                if user_OTP.save():
                    msg = send_mail(
                        'WasteCoin OTP verification',
                        'Hello ' + firstName + " " + lastName + "\n Your OTP confirmation code is: \n " + code + " \n Use this code to verify your registration. WasteCoin will never ask you to share this code with anyone.",
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                    return msg

                    if msg:
                        return_data = {
                            "error": "0",
                            "message":"The registration was successful",
                            "user_id": f"{userRandomId}",
                            "OTP_Code": f"{code}"
                        }
                        
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": "An Error Occured"
        }
    return Response(return_data)

@api_view(["POST"])
@autentication.user_tokenid
def user_verification(request,user_id):
    try:
        otp_entered = request.data.get("otp")
        if otp_entered is not None and otp_entered is not "":
            user_data = otp.objects.get(user__user_id=user_id)
            otpCode,date_added = str(user_data.otp_code),user_data.date_added
            date_now = datetime.now(timezone.utc)
            duration = float((date_now - date_added).total_seconds())
            timeLimit = 1800.0 #30 mins interval
            if otp_entered == otpCode and duration < timeLimit:
                #validate user
                user_data.validated = True
                user_data.save()
                return_data = {
                    "error": "0",
                    "message":"User Verified"
                }
            elif otp_entered != otpCode and duration < timeLimit:
                return_data = {
                    "error": "1",
                    "message": "Incorrect OTP"
                }
            elif otp_entered == otpCode and duration > timeLimit:
                #We should generate another and send to the user here
                newOTP = string_generator.numeric(6)
                user_data.otp_code = newOTP
                user_data.save()
                return_data = {
                    "error": "1",
                    "message": "OTP has expired"
                }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameters"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return Response(return_data)

@api_view(["POST"])
def user_login(request):
    try:
        email_phone = request.data.get("email_phone")
        password = request.data.get("password")
        field = [email_phone,password]
        if not None in field and not '' in field:
            validate_mail = validator.checkmail(email_phone)
            if validate_mail == True:
                if User.objects.filter(email =email_phone).exists() == False:
                    return_data = {
                        "error": "1",
                        "message": "User does not exist"
                    }
                else:
                    user_data = User.objects.get(email=email_phone)
                    is_valid_password = password_functions.check_password_match(password,user_data.user_password)
                    is_verified = otp.objects.get(user__user_phone=user_data.user_phone).validated
                    if is_valid_password and is_verified:
                        return_data = {
                            "error": "0",
                            "message": "Successfull"
                            }
                    elif is_verified == False:
                        return_data = {
                            "error" : "1",
                            "message": "User is not verified"
                        }
                    else:
                        return_data = {
                            "error" : "1",
                            "message" : "Wrong Password"
                        }
            else:
                if User.objects.filter(user_phone =email_phone).exists() == False:
                    return_data = {
                        "error": "1",
                        "message": "User does not exist"
                    }
                else:   
                    user_data = User.objects.get(user_phone=email_phone)
                    is_valid_password = password_functions.check_password_match(password,user_data.user_password)
                    is_verified = otp.objects.get(user__user_phone=user_data.user_phone).validated
                    if is_valid_password and is_verified:
                        return_data = {
                            "error": "0",
                            "message": "Successfull"
                        }
                    elif is_verified == False:
                        return_data = {
                            "error" : "1",
                            "message": "User is not verified"
                        }
                    else:
                        return_data = {
                            "error" : "1",
                            "message" : "Wrong Password"
                        }
        else:
            return_data = {
                "error" : "2",
                "message" : "Invalid Parameters"
                }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return Response(return_data)


