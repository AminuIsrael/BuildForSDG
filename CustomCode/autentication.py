from rest_framework.response import Response
from rest_framework import status
import jwt
from wasteCoin import settings

def token_required(something):
    def wrap(request):
        try:
            if request.META['HTTP_TOKEN'] != '' and request.META['HTTP_TOKEN'] != None:
                token_passed = request.META['HTTP_TOKEN']
                try:
                    data = jwt.decode(token_passed,settings.SECRET_KEY, algorithms=['HS256'])
                    return something(request,data)
                except jwt.exceptions.ExpiredSignatureError:
                    return_data = {
                        "error": "1",
                        "message": "Token has expired"
                        }
                    return Response(return_data, status=status.HTTP_401_UNAUTHORIZED)
                except:
                    return_data = {
                        "error": "1",
                        "message": "Invalid Token"
                    }
                    return Response(return_data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return_data = {
                    "error" : "2",
                    "message" : "Token required",
                    }
                return Response(return_data, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return_data = {
                "error" : "3",
                "message" : "An error occured"
                }
            return Response(return_data, status=status.HTTP_401_UNAUTHORIZED)
    return wrap
                
                
