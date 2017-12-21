from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from channels.models import Channel, Category


class ChannelAPITestCase(APITestCase):
    def setUp(self):
        """
        Setup data in the database to test API endpoints
        """
        categories = [
            ['Home & Garden',
             'Kitchen & Dining',
             'Kitchen Tools & Utensils',
             'Food Graters & Zesters'],
            ['Home & Garden',
             'Household Appliances',
             'Laundry Appliances',
             'Dryers'],
        ]

        bar = Channel.objects.create(name='bar')
        bar.add_category(categories[0])
        baz = Channel.objects.create(name='baz')
        baz.add_category(categories[0])

        self.channel = Channel.objects.create(name='foo')
        self.channel.add_category(categories[1])
        self.category = Category.objects.get(parent=self.channel, name='Home & Garden')

    def test_get_channels_list(self):
        """
        Get the list of all channels
        """
        url = reverse('channel-list')
        response = self.client.get(url)
        data = response.data
        base_url = response.wsgi_request.build_absolute_uri()
        expected = [
            {'url': base_url + 'foo/', 'name': 'foo'},
            {'url': base_url + 'baz/', 'name': 'baz'},
            {'url': base_url + 'bar/', 'name': 'bar'},
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected)

    def test_get_channel_detail(self):
        """
        Get a channel details
        """
        channel_url = reverse('channel-detail', args=['foo'])
        response = self.client.get(channel_url)
        data = response.data
        # check response code and response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('url', data)
        self.assertIn('name', data)
        self.assertIn('subcategories_count', data)
        self.assertIn('subcategories', data)
        self.assertIn('url', data['subcategories'][0])
        self.assertIn('name', data['subcategories'][0])
        self.assertIn('path', data['subcategories'][0])

    def test_get_channel_detail_should_be_case_insensitive(self):
        url = reverse('channel-detail', args=['Foo'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_list(self):
        """
        Get the list of all categories
        """
        url = reverse('category-list')
        response = self.client.get(url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 12)
        self.assertIn('url', data[0])
        self.assertIn('name', data[0])
        self.assertIn('path', data[0])
        self.assertIn('channel', data[0])

    def test_get_category_detail_with_subcategories(self):
        """
        Get a category details
        """
        url = reverse('category-detail', args=[self.category.pk])
        response = self.client.get(url)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('url', data)
        self.assertIn('name', data)
        self.assertIn('path', data)
        self.assertIn('channel', data)
        self.assertIn('parent', data)
        self.assertIn('subcategories_count', data)
        self.assertIn('subcategories', data)
        self.assertIn('url', data['subcategories'][0])
        self.assertIn('name', data['subcategories'][0])
        self.assertIn('path', data['subcategories'][0])

    def test_channel_detail_does_not_exist(self):
        """
        If the channel does not exist return 404 code
        and reason of error
        """
        url = reverse('channel-detail', args=['this does not exist'])
        response = self.client.get(url)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)

    def test_category_does_not_exist(self):
        """
        If the category does not exist return 404 code and reason of error
        """
        url = reverse('category-detail', args=['1231234'])
        response = self.client.get(url)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)

    def test_search_channels(self):
        """
        Search all channels that contain the keyword in the name
        """
        # channels that contains 'ba' in the name
        url = reverse('channel-list') + '?search=ba'
        response = self.client.get(url)
        bar_url = response.wsgi_request.build_absolute_uri(reverse('channel-detail', args=['bar']))
        baz_url = response.wsgi_request.build_absolute_uri(reverse('channel-detail', args=['baz']))
        expected = [
            {'url': baz_url, 'name': 'baz'},
            {'url': bar_url, 'name': 'bar'},
        ]
        self.assertEqual(response.data, expected)

    def test_empty_channel_search_result(self):
        """
        When nothing is found return empty result
        """
        url = reverse('channel-list') + '?search=this channel does not exist'
        response = self.client.get(url)
        expected = []
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_search_categories(self):
        """
        Search all categories that contain the keyword
        """
        url = reverse('category-list') + '?search=appliances'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_empty_category_search_result(self):
        """
        When nothing is found return 404 code and reason
        """
        url = reverse('category-list') + '?search=no existe'
        response = self.client.get(url)
        expected = []
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_root_redirect_to_api_docs(self):
        """
        Root url page should redirect to api docs
        """
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/api/v1/docs/')
