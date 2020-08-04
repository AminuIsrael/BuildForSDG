from django.test import TestCase
from django.utils import timezone
from api.models import User, ContactUs,otp

class TestUser(TestCase):
    create_user= User(user_id="Iral8PHTGkfuyb1hv9Xz",firstname="john",lastname="wilson",email="johnwilson@gmail.com",
                         user_phone="09017373728",user_gender="Male",user_password="123456789",user_address="Wilson Street",
                         user_state="Lagos",user_LGA="Ojo",user_country="Nigeria")
    
    def test_user_fetch(self):
        self.assertEqual(self.create_user.user_id,"Iral8PHTGkfuyb1hv9Xz")
        self.assertEqual(self.create_user.firstname,"john")
        self.assertEqual(self.create_user.email,"johnwilson@gmail.com")
        self.assertNotEqual(self.create_user.date_added,timezone.now)
        self.assertEqual(self.create_user.role,"user")
        
        
class TestOtp(TestUser):
    
    def test_otp(self):
        user_otp = otp(user=self.create_user,otp_code="123456")
        self.assertEqual(user_otp.otp_code,"123456")
        self.assertIs(user_otp.validated,False)
        #Check if otp belongs to user
        self.assertEqual(user_otp.user.firstname,"john")
        #Check time of saving data
        self.assertNotEqual(self.create_user.date_added,timezone.now)