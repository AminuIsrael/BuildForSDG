from django.urls import path
from api import views

urlpatterns = [
    path('',views.index_page),
    path('signup',views.user_registration),
    path('signin',views.user_login)
]