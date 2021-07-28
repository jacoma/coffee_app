# Create your tests here.

from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from .views import add_coffee, home, user_profile, user_home
from .models import User, coffee_ratings, coffee_details

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class UserProfileTests(TestCase):
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
        self.assertEquals(view.func, user_home)


class NewCoffeeTests(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='Django', password='1X<ISRUkw+tuK', email = 'django@gmail.com')
        test_user1.save()

    def test_new_topic_view_success_status_code(self):
        url = reverse('add_coffee', kwargs={'username': 'Django'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('add_coffee', kwargs={'username': 'about'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/user/Django/add-coffee/')
        self.assertEquals(view.func, add_coffee)

    #def test_new_topic_view_contains_link_back_to_board_topics_view(self):
     #   new_topic_url = reverse('new_topic', kwargs={'pk': 1})
    #    board_topics_url = reverse('board_topics', kwargs={'pk': 1})
     #   response = self.client.get(new_topic_url)
     #   self.assertContains(response, 'href="{0}"'.format(board_topics_url))