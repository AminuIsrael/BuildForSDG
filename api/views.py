import jwt
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import User,otp,UserCoins,LeaderBoard,ExchangeRate,UserTrasactionHistory
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
                transactionid = string_generator.numeric()
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
                #Save Transaction Details
                user_transaction = UserTrasactionHistory(user=new_userData,transaction_id=transactionid,
                                                        amount=0,transaction="Credit")
                user_transaction.save()
                #Generate token
                timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=120) #set limit for user
                payload = {"user_id": f"{userRandomId}",
                           "exp":timeLimit}
                token = jwt.encode(payload,settings.SECRET_KEY)
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
        user_id = decrypedToken['user_id']
        if user_id != None and user_id != '':
            user_data = UserCoins.objects.get(user__user_id=user_id)
            user_coins = user_data.allocateWasteCoin
            month = user_data.date_added.strftime('%B') 
            rate = ExchangeRate()
            exchangeRate,changed_rate = rate.exchangeRate,rate.changedRate
            minedCoins = user_data.minedCoins
            unminedCoins = user_coins - minedCoins
            miner_id = LeaderBoard.objects.get(user__user_id=user_id).minerID
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

@api_view(["GET"])
def LeadBoard(request):
    try:
        WasteCoinBoard = LeaderBoard.objects.all().order_by('-minedCoins')
        i = 0
        topCoinsMined = []
        numberOfUsers = 5
        while i < numberOfUsers:
            topUsers = {
                "miner_id": WasteCoinBoard[i].minerID,
                "CoinMined": WasteCoinBoard[i].minedCoins
            }
            topCoinsMined.append(topUsers)
            i += 1
        return_data = {
            "error": "0",
            "message": "Successfull",
            "LeaderBoard": topCoinsMined
        }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": str(e)
        }
    return Response(return_data)

@api_view(["GET"])
@autentication.token_required
def user_profile(request,decrypedToken):
    try:
        userID = decrypedToken['user_id']
        UserInfo = User.objects.get(user_id=userID)
        UserCoin = UserCoins.objects.get(user__user_id=userID)
        UserMine = LeaderBoard.objects.get(user__user_id=userID)
        return_data = {
            "error": "0",
            "message": "Successfull",
            "user_data": [
                {
                    "user_details": [
                        {
                            "first_name": f"{UserInfo.firstname}",
                            "last_name": f"{UserInfo.lastname}",
                            "email": f"{UserInfo.email}",
                            "phone_number": f"{UserInfo.user_phone}",
                            "gender": f"{UserInfo.user_gender}",
                            "address": f"{UserInfo.user_address}",
                            "state": f"{UserInfo.user_state}",
                            "LGA": f"{UserInfo.user_LGA}",
                            "country": f"{UserInfo.user_country}"
                              
                        }
                    ],
                    "user_coins": [
                        {
                            "miner_id": f"{UserMine.minerID}",
                            "allocatedCoin": f"{UserCoin.allocateWasteCoin}",
                            "minedcoins": f"{UserCoin.minedCoins}"
                        }
                    ]
                }
            ]
        }
        
    except Exception as e:
        return_data = {
            "error": "0",
            "message": str(e)
        }
    return Response(return_data)

@api_view(["POST"])
@autentication.token_required
def wallet_transactions(request,decrypedToken):
    pass


# @api_view(["POST"])
# @autentication.token_required
# def allocate_coins(request,decrypedToken):
#     try:
#         coins_allocated = request.data.get("coins_allocated")
#         #email of user to allocate coins to
#         user_email = request.data.get("userEmail")
#         if coins_allocated != None and coins_allocated != "":
#             #Check if user is an admin
#             user_identity = User.objects.get(user_id= decrypedToken['user_id'])
#             user_role = user_identity.role
#             if user_role != "admin":
#                 return_data = {
#                     "error": "0",
#                     "message": "Unauthorized User"
#                 }
#             else:
#                 #get user info
#                 wastecoin_user = UserCoins.objects.get(user__email=user_email)
#                 if User.objects.filter(email =user_email).exists() == False:
#                     return_data = {
#                     "error": "1",
#                     "message": "User does not exist"
#                 }
                
#     except Exception as e:
#         return_data = {
#             "error": "3",
#             "message": "An error occured"
#         }