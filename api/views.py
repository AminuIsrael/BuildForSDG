from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from api.models import User,otp
from CustomCode import string_generator,password_functions


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
def user_login(request):
    try:
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        field = [phone_number,password]
        if not None in field and not '' in field:
            if User.objects.filter(user_phone =phone_number).exists() == False:
                return_data = {
                    "error": "1",
                    "message": "User does not exist or Invalid Phone Number"
                }
            else:
                user_data = User.objects.get(user_phone=phone_number)
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
            "message": "An error occured"
        }
    return Response(return_data)