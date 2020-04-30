from django.urls import path
from api import views

urlpatterns = [
    path('',views.index_page),
    path('api/v1/signup',views.user_registration),
    path('api/v1/signin',views.user_login)
]