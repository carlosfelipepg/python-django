from datetime import timedelta
from typing import OrderedDict
import uuid
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from news.serializers import NewsSerializer
from link.models import Link
from news.models import News

class LinkAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('link-api')
        self.news_data = {
            'title': 'Test News Article',
            'content': 'This is a test news article.',
            'author': 'John Doe',
        }        
        self.news = News.objects.create(**self.news_data)

        self.link_data = {
            'token': str(uuid.uuid4())[:12],
            'news': self.news,
            'expiration_date': timezone.now() + timedelta(hours=1),
        }
        self.link = Link.objects.create(**self.link_data)

    def test_create_link(self):
        body = {
            'news_id': self.news.id
        }
        response = self.client.post(self.url, body, format='json')
  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('link', response.data)
    
    def test_get_news_by_link(self):
        url = reverse('link-api-token', args=[self.link.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = NewsSerializer(self.news, many=False).data
        self.assertEqual(response.data, expected_data)

    def test_get_expired_link(self):
        link_data = {
            'token': str(uuid.uuid4())[:12],
            'news': self.news,
            'expiration_date': timezone.now() + timedelta(hours=-1),
        }
        link = Link.objects.create(**link_data)
        url = reverse('link-api-token', args=[link.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_data = {
            'message': 'link expired'
        }
        self.assertEqual(response.data, expected_data)

