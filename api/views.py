from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render


# Create your views here.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error" : "0",
        "message" : "Successful",
    }
    return Response(return_data)



