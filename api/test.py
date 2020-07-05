from django.test import TestCase
from api.models import User
from django.utils import timezone

# Create your tests here
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(user_id='h7YbViN8J1TezScP4gLE',firstname="Israel",lastname="Aminu",
                            email='aminuisrael@gmail.com',user_phone='09017373729',
                            user_gender="Male",user_password="123456789",user_address="Kolawole Street",
                            user_state= "Lagos", user_LGA= "Ojo",user_country="Nigeria",date_added=timezone.now)

        
    def test_db_fetch(self):
        "Fetching Data from the Database"
        user = User.objects.get(user_id='h7YbViN8J1TezScP4gLE')
        self.assertEqual(user.firstname, "Israel")
        self.assertEqual(user.lastname,"Aminu")
        self.assertEqual(user.email,"aminuisrael2@gmail.com")
        self.assertEqual(user.user_phone,'09017373729')
        self.assertEqual(user.user_gender,"Male")
        self.assertEqual(user.user_password,"123456789")
        self.assertEqual(user.user_address,"Kolawole Street")
        self.assertEqual(user.user_state,"Lagos")
        self.assertEqual(user.user_LGA,"Ojo")
        self.assertEqual(user.user_country,"Nigeria")
        self.assertNotEqual(user.date_added,timezone.now)
        self.assertEqual(user.role,"user")
        