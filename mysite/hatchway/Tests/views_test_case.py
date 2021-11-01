from django.http import HttpResponseServerError
from django.test import TestCase, Client
from ..Providers.posts import Posts
from ..views import *
from typing import List, Dict
# Create your tests here.
client = Client()
class ViewsTestCase(TestCase):
    
    def test_ping(self):
        response = client.get('/api/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success":True})
    
    def test_direction_invalid_query_argument(self):
        response = client.get('/api/posts?tags=history,tech&direction=ascending&sortBy=likes')
        self.assertEqual(response.status_code, 400)
    
    def test_direction_valid_query_argument(self):
        response = client.get('/api/posts?tags=history,tech&direction=asc&sortBy=likes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), dict)
    
    def test_sort_by_invalid_query_argument(self):
        response = client.get('/api/posts?tags=history,tech&direction=asc&sortBy=like')
        self.assertEqual(response.status_code, 400)
    
    def test_sort_by_valid_query_argument(self):
        response = client.get('/api/posts?tags=history,tech&direction=asc&sortBy=likes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), dict)

    def test_tags_parameter_not_present(self):
        response = client.get('/api/posts?direction=asc&sortBy=likes')
        self.assertEqual(response.status_code, 400)
        
    def test_tags_parameter_present_with_invalid_tag(self):
        response = client.get('/api/posts?tags=biology&direction=asc&sortBy=likes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'posts':[]})
