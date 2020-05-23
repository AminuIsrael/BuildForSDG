from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class User(models.Model):
    class Meta:
        db_table = "WasteCoin_user_table"
    user_id = models.CharField(max_length=500,unique=True)
    firstname = models.CharField(max_length=30,verbose_name="Firstname",blank=True)
    lastname = models.CharField(max_length=30,verbose_name="Lastname",blank=True)
    email = models.EmailField(max_length=90, unique=True,verbose_name="Email")
    user_phone = models.CharField(max_length=15, unique=True, null=True, verbose_name="Telephone number")
    user_gender = models.CharField(max_length=15, verbose_name="Gender")
    user_password = models.TextField(max_length=200,verbose_name="Password")
    user_address = models.TextField(max_length=200,verbose_name="Address")
    user_state = models.TextField(max_length=200,verbose_name="State")
    user_LGA = models.TextField(max_length=200,verbose_name="State")
    user_country = models.TextField(max_length=200,verbose_name="Country")
    date_added = models.DateTimeField(default=timezone.now)
    role = models.TextField(max_length=50,verbose_name="User role",default="user")
    
class otp(models.Model):
    class Meta:
        db_table = "OTP_Code"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password_reset_code = models.TextField(max_length=20,verbose_name="Reset Code",default="")
    date_added = models.DateTimeField(default=timezone.now)


class UserCoins(models.Model):
    class Meta:
        db_table = "User_Coins"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    allocateWasteCoin = models.IntegerField(verbose_name="AllocatedWasteCoin",default=0)
    minedCoins = models.IntegerField(verbose_name="minedCoins",default=0)
    date_added = date_added = models.DateTimeField(default=timezone.now)

class LeaderBoard(models.Model):
    class Meta:
        db_table = "WC_LeaderBoard"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    minerID = models.CharField(max_length=500,unique=True,verbose_name="miner_ID")
    minedCoins = models.IntegerField(default=0,verbose_name="mined_Coins")

class ExchangeRate(models.Model):
    class Meta:
        db_table = "Exchange_Rate"
    exchangeRate = models.FloatField(default=0,verbose_name="exchangeRate")
    changedRate = models.FloatField(default=0,verbose_name="changedRate")
    