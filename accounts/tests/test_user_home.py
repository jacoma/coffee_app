from django.urls import reverse, resolve
from django.test import TestCase
from accounts import views as accounts_views
from django.contrib.auth.models import User

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, accounts_views.home)

class UserHomeTests(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='Django', password='1X<ISRUkw+tuK', email = 'django@gmail.com')
        test_user1.save()

    def test_user_profile_view_success_status_code(self):
        url = reverse('user_home', kwargs={'username': 'Django'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_user_profile_view_not_found_status_code(self):
        url = reverse('user_home', kwargs={'username': 'about'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_user_profile_url_resolves_user_profile_view(self):
        view = resolve('/user/Django/')
        self.assertEquals(view.func, accounts_views.user_home)