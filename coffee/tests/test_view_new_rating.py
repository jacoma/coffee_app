from django.test import TestCase
from django.urls import resolve, reverse
from ..models import *
from accounts.views import user_home


class UserHomeTests(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='Django', password='1X<ISRUkw+tuK', email = 'django@gmail.com')
        test_user1.save()

    def test_user_home_view_success_status_code(self):
        url = reverse('user_home', kwargs={'username': 'Django'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_user_home_view_not_found_status_code(self):
        url = reverse('user_home', kwargs={'username': 'about'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_user_home_url_resolves_user_home_view(self):
        view = resolve('/user/Django/')
        self.assertEquals(view.func, user_home)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))

class LoginRequiredNewRatingTests(TestCase):
    def setUp(self):
        dim_coffee.objects.create(name='Django', roaster='Django board.')
        self.url = reverse('add_rating', kwargs={'username': 'Django'})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))