from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from channels.models import Channel


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
        Channel.create('bar').add_category(categories[0])
        baz = Channel.create('baz')
        baz.add_category(categories[0])
        self.category_pk = baz.add_category(categories[1]).pk
        self.channel = Channel.create('foo')
        self.channel.add_category(categories[1])

    def test_get_channels_list(self):
        """
        Get the list of all channels
        """
        url = reverse('channel-list')
        response = self.client.get(url)
        base_url = response.wsgi_request.build_absolute_uri()
        expected = [
            {'url': base_url + 'bar/', 'name': 'bar'},
            {'url': base_url + 'baz/', 'name': 'baz'},
            {'url': base_url + 'foo/', 'name': 'foo'},
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_get_channel_detail(self):
        """
        Get a channel details
        """
        url = reverse('channel-detail', args=['foo'])
        response = self.client.get(url)
        channel_url = response.wsgi_request.build_absolute_uri()
        expected = {
            'url': channel_url,
            'name': 'foo',
            'categories': [
                'Home & Garden',
                'Home & Garden/Household Appliances',
                'Home & Garden/Household Appliances/Laundry Appliances',
                'Home & Garden/Household Appliances/Laundry Appliances/Dryers'
            ],
            'categories_count': 4,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

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

    def test_get_category_detail(self):
        """
        Get a category details
        """
        url = reverse('category-detail', args=[self.category_pk])
        response = self.client.get(url)
        category_url = response.wsgi_request.build_absolute_uri()
        channel_category = response.wsgi_request.build_absolute_uri(reverse('channel-detail', args=['baz']))
        expected = {
            'url': category_url,
            'name': 'Dryers',
            'path': 'Home & Garden/Household Appliances/Laundry Appliances/Dryers',
            'subcategories': [

            ],
            'channel': channel_category,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        url = reverse('search-channel', args=['ba'])
        response = self.client.get(url)
        bar_url = response.wsgi_request.build_absolute_uri(reverse('channel-detail', args=['bar']))
        baz_url = response.wsgi_request.build_absolute_uri(reverse('channel-detail', args=['baz']))
        expected = [
            {'url': bar_url, 'name': 'bar'},
            {'url': baz_url, 'name': 'baz'},
        ]
        self.assertEqual(response.data, expected)

    def test_empty_channel_search_result(self):
        """
        When nothing is found return 404 code and reason
        """
        url = reverse('search-channel', args=['this channel does not exist'])
        response = self.client.get(url)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)

    def test_search_categories(self):
        """
        Search all categories that contain the keyword
        """
        url = reverse('search-category', args=['appliances'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_empty_category_search_result(self):
        """
        When nothing is found return 404 code and reason
        """
        url = reverse('search-category', args=['this category does not exist'])
        response = self.client.get(url)
        expected = {'detail': 'Not found.'}
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, expected)

    def test_root_redirect_to_api_docs(self):
        """
        Root url page should redirect to api docs
        """
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/api/v1/docs/')

    def test_get_category_detail_with_subcategories(self):
        """
        Check for correctness in subcategories of category
        """
        category = self.channel.get_category('Household Appliances')
        url = reverse('category-detail', args=[category.pk])
        response = self.client.get(url)
        category_url = response.wsgi_request.build_absolute_uri()
        channel_category = response.wsgi_request.build_absolute_uri(reverse('channel-detail', args=['foo']))
        expected = {
            'url': category_url,
            'name': 'Household Appliances',
            'path': 'Home & Garden/Household Appliances',
            'subcategories': [
                'Home & Garden/Household Appliances/Laundry Appliances',
                'Home & Garden/Household Appliances/Laundry Appliances/Dryers'
            ],
            'channel': channel_category,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)