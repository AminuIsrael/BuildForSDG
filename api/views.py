import jwt
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import User,otp,UserCoins,LeaderBoard,ExchangeRate
from wasteCoin import settings
from CustomCode import string_generator,password_functions,validator,autentication,send_email

# Create your views here.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error" : "0",
        "message" : "Successful"
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
                miner_id = string_generator.numeric(7)
                user_token = string_generator.alphanumeric(50)
                #encrypt password
                encryped_password = password_functions.generate_password_hash(password)
                #Save user_data
                new_userData = User(user_id=userRandomId,firstname=firstName,lastname=lastName,
                                email=email,user_phone=phoneNumber,user_gender=gender,
                                user_password=encryped_password,user_address=address,
                                user_state=state,user_LGA=lga,user_country=country)
                new_userData.save()
                #Save OTP
                user_OTP =otp(user=new_userData)
                user_OTP.save()
                #Generate default coins
                user_Coins = UserCoins(user=new_userData)
                user_Coins.save()
                #add to leaderBoard
                user_Board = LeaderBoard(user=new_userData,minerID=miner_id)
                user_Board.save()
                #Generate token
                timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=120) #set limit for user
                payload = {"user_id": f"{userRandomId}",
                           "exp":timeLimit}
                token = jwt.encode(payload,settings.SECRET_KEY)
                #send_email.send_email("WasteCoin OTP verification",email,' Hello ' + firstName + ",\nWelcome to WasteCoin,"+ "\nYour OTP verification code is: \n " +code + " \nUse this code to verify your registration. WasteCoin will never ask you to share this code with anyone."+ "\n\n Yours Sincerely," + "\n The WasteCoin Team.")
                return_data = {
                    "error": "0",
                    "message": "The registration was successful",
                    "token": f"{token.decode('UTF-8')}",
                    "elapsed_time": f"{timeLimit}",
                    }
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return Response(return_data)

#User login
@api_view(["POST"])
def user_login(request):
    try:
        email_phone = request.data.get("email_phone",None)
        password = request.data.get("password",None)
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
                    #Generate token
                    timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=120) #set limit for user
                    payload = {"user_id": f'{user_data.user_id}',
                               "exp":timeLimit}
                    token = jwt.encode(payload,settings.SECRET_KEY)
                    if is_valid_password:
                        return_data = {
                            "error": "0",
                            "message": "Successfull",
                            "token": token.decode('UTF-8'),
                            "token-expiration": f"{timeLimit}",
                            "user_details": [
                                {
                                    "firstname": f"{user_data.firstname}",
                                    "lastname": f"{user_data.lastname}",
                                    "email": f"{user_data.email}",
                                    "phone_number": f"{user_data.user_phone}",
                                    "gender": f"{user_data.user_gender}",
                                    "address": f"{user_data.user_address}",
                                    "state": f"{user_data.user_state}",
                                    "LGA": f"{user_data.user_LGA}",
                                    "country": f"{user_data.user_country}"
                                    
                                }
                            ]
                            
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
                    #Generate token
                    timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=120) #set limit for user
                    payload = {"user_id": f'{user_data.user_id}',
                               "exp":timeLimit}
                    token = jwt.encode(payload,settings.SECRET_KEY)
                    if is_valid_password:
                        return_data = {
                            "error": "0",
                            "message": "Successfull",
                            "token": token.decode('UTF-8'),
                            "token-expiration": f"{timeLimit}",
                            "user_details": [
                                {
                                    "firstname": f"{user_data.firstname}",
                                    "lastname": f"{user_data.lastname}",
                                    "email": f"{user_data.email}",
                                    "phone_number": f"{user_data.user_phone}",
                                    "gender": f"{user_data.user_gender}",
                                    "address": f"{user_data.user_address}",
                                    "state": f"{user_data.user_state}",
                                    "LGA": f"{user_data.user_LGA}",
                                    "country": f"{user_data.user_country}"
                                    
                                }
                            ]
                            
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

#send email to change password
@api_view(["POST"])
def password_reset(request):
    try:
        emailAddress = request.data.get('emailaddress',None)
        if emailAddress is not None and emailAddress is not "":
            if User.objects.filter(email =emailAddress).exists() == False:
                return_data = {
                    "error": "1",
                    "message": "User does not exist"
                }
            else:
                user_data = otp.objects.get(user__email=emailAddress)
                generate_pin = string_generator.alphanumeric(15)
                user_data.password_reset_code = generate_pin
                user_data.save()
                #send_email.send_email('WasteCoin Reset Password',emailAddress,' Hello ' + "\nYour Reset Password code is: \n " +generate_pin + " \nUse this code to verify your registration. WasteCoin will never ask you to share this code with anyone."+ "\n\n Yours Sincerely," + "\n The WasteCoin Team.")
                return_data = {
                    "error": "0",
                    "message": "Successful, Email sent",
                    "code": f"{generate_pin}"
                }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return Response(return_data)

#Change password
@api_view(["POST"])
@autentication.token_required
def password_change(request,decrypedToken):
    try:
        reset_code = request.data.get("reset_code")
        new_password = request.data.get("new_password")
        fields = [reset_code,new_password]
        if not None in fields and not "" in fields:
            #get user info
            user_data = User.objects.get(user_id=decrypedToken["user_id"])
            otp_reset_code = otp.objects.get(user__user_id=decrypedToken["user_id"]).password_reset_code
            print(otp_reset_code)
            if reset_code == otp_reset_code:
                #encrypt password
                encryptpassword = password_functions.generate_password_hash(new_password)
                user_data.user_password = encryptpassword
                user_data.save()
                return_data = {
                    "error": "0",
                    "message": "Successfull, Password Changed"
                }
            elif reset_code != otp_reset_code:
                return_data = {
                    "error": "1",
                    "message": "Code does not Match"
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
@autentication.token_required
def Dashboard(request,decrypedToken):
    try:
        if decrypedToken['user_id'] != None and decrypedToken['user_id'] != '':
            user_data = UserCoins.objects.get(user__user_id=decrypedToken["user_id"])
            user_coins = user_data.allocateWasteCoin
            month = user_data.date_added.strftime('%B') 
            rate = ExchangeRate()
            exchangeRate,changed_rate = rate.exchangeRate,rate.changedRate
            minedCoins = user_data.minedCoins
            unminedCoins = user_coins - minedCoins
            miner_id = LeaderBoard.objects.get(user__user_id=decrypedToken["user_id"]).minerID
            return_data = {
                "error": "0",
                "message": "Sucessfull",
                "data": [
                    {
                        "allocatedWasteCoin": user_coins,
                        "month": month,
                        "exchangeRate": exchangeRate,
                        "changedRate": changed_rate,
                        "summary": [
                            {
                                "mined": minedCoins,
                                "unMined": unminedCoins
                            }
                        ],
                        "totalWasteCoinMined": minedCoins,
                        "leaderBoard":[
                            {
                                "minerId": miner_id,
                                "wasteCoinsMined": minedCoins
                            }
                        ]
                    }
                ]
            }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameter"
            } 
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return Response(return_data)


