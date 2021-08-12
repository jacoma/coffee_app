from django.urls import reverse, resolve
from django.test import TestCase
from ..views import add_coffee
from ..models import User, dim_coffee, ratings

class NewCoffeeTests(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='Django', password='1X<ISRUkw+tuK', email = 'django@gmail.com')
        test_user1.save()

    def test_new_coffee_view_success_status_code(self):
        url = reverse('add_coffee', kwargs={'username': 'Django'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_coffee_view_not_found_status_code(self):
        url = reverse('add_coffee', kwargs={'username': 'about'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_coffee_url_resolves_new_coffee_view(self):
        view = resolve('/user/Django/add-coffee/')
        self.assertEquals(view.func, add_coffee)

    def test_csrf(self):
        url = reverse('add_coffee', kwargs={'username': 'Django'})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_coffee_valid_post_data(self):
        url = reverse('add_coffee', kwargs={'username': 'Django'})
        data = {
            'name': 'Test Coffee',
            'roaster': 'Test Roaster'
        }
        response = self.client.post(url, data)
        self.assertTrue(dim_coffee.objects.exists())

    def test_new_coffee_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('add_coffee', kwargs={'username': 'Django'})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_coffee_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('add_coffee', kwargs={'username': 'Django'})
        data = {
            'name': '',
            'roaster': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(dim_coffee.objects.exists())

    #def test_new_topic_view_contains_link_back_to_board_topics_view(self):
     #   new_topic_url = reverse('new_topic', kwargs={'pk': 1})
    #    board_topics_url = reverse('board_topics', kwargs={'pk': 1})
     #   response = self.client.get(new_topic_url)
     #   self.assertContains(response, 'href="{0}"'.format(board_topics_url))
