from django.test import TestCase
from gestionAnnonce.servises import AuthManager,MessagManager ,FavoriteManager
from gestionAnnonce.models import User ,Annoncement,Category,Type ,Contact,Location,Address,Wilaya,Commune


class Testauthmanger(TestCase):

    def test_login(self):
       token1 = AuthManager.login(email="imane.haissam3@gmail.com",family_name="test" ,first_name="test",image="")
       token2 = AuthManager.login(email="imane.haissam3@gmail.com",family_name="test" ,first_name="test",image="")
       token3 = AuthManager.login(email="mm",family_name="imane" ,first_name="haissam",image="")
       self.assertEqual(token1,token2)
       self.assertEqual(500,token3)

class TestMessagManager(TestCase):
    def setUp(self):
        User.objects.create(email="test1@gmail.com",first_name="test",family_name="test",image="")
        User.objects.create(email="test2@gmail.com",first_name="test",family_name="test",image="")

    def test_sendmessage(self):
        sending_user=User.objects.get(email="test1@gmail.com")
        recieving_user=User.objects.get(email="test2@gmail.com")
        message = MessagManager.send_message(sending_user.id , recieving_user.id, content="test_content",title="test_title")
        self.assertEqual(message.content,"test_content")
        self.assertEqual(message.title,"test_title")
        self.assertEqual(message.sent_by,sending_user)
        self.assertEqual(message.sent_to,recieving_user)

class TestFavoriteManager(TestCase):
    def setUp(self):
        annonce=Annoncement.objects.create(
            title= "test_title",
            category = Category.objects.create(cat_name="test_cat"),
            type= Type.objects.create(type_name="test_type"),
            user=User.objects.create(email="test1@gmail.com",first_name="test",family_name="test",image=""),
            area= 123,
            price=122,
            creation_date="2023-02-03T15:35:51.760316Z",
            description= "test_description",
            deleted =False,
            contact=Contact.objects.create(
            first_name = "test_name",
            family_name = "test_last_name",
            address = "personal_address",
            phone ="0823",
            mail ="test@gmail.com"
        ),
        location=Location.objects.create(
            wilaya=Wilaya.objects.create(designation="test"),
            commune=Commune.objects.create(designation="test",wilaya=Wilaya.objects.get(designation="test")),
            address=Address.objects.create(
                address= "address",
                latitude= 0.0,
                longitude=0.0,
            )
        )
        )
        User.objects.create(email="test2@gmail.com",first_name="testfav",family_name="testfav",image="")

    def test_add_favorate(self):
        user=User.objects.get(email="test2@gmail.com")
        id_announcement =Annoncement.objects.get(title= "test_title").id
        annoncement =FavoriteManager.add_favorate(user.id,id_announcement)
        print(user.id)
        print(id_announcement)
        print(annoncement.favorated_by)
        self.assertTrue(annoncement.favorated_by.contains(user))
        



