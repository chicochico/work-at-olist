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

    def test_get_category_detail(self):
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

    def test_category_does_not_exist(self):
        """
        If the category does not exist return 404 code and reason of error
        """
        url = reverse('category-detail', args=['1231234'])
        response = self.client.get(url)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)
