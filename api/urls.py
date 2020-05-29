from django.urls import path
from api import views

urlpatterns = [
    path('',views.index_page),
    path('api/v1/signup',views.user_registration),
    path('api/v1/signin',views.user_login),
    path('api/v1/password_reset',views.password_reset),
    path('api/v1/password_change',views.password_change),
    path('api/v1/dashboard',views.Dashboard),
    path('api/v1/leaderboard',views.LeadBoard),
    path('api/v1/profile',views.user_profile),
    path('api/v1/wallet',views.wallet_details),
    path('api/v1/redeem',views.redeemcoins),
    path('api/v1/allocate',views.allocate_coins)
]