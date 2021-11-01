from django.http import HttpResponseServerError
from django.test import TestCase, Client
from ..Providers.posts import Posts
from ..views import *
from typing import List, Dict
# Create your tests here.

class PostsProviderTestCase(TestCase):
    
    def test_sort_by_id_asc_and_remove_duplicates(self):
        posts: Posts = Posts(direction='asc', sort_by='id')
        posts.posts_data += [
        {'id':1, 'reads':200, 'likes':300, 'popularity':234},
        {'id':5, 'reads':100, 'likes':356, 'popularity':53}, 
        {'id':0, 'reads':0, 'likes':32, 'popularity':10},
        {'id':5, 'reads':100, 'likes':356, 'popularity':53}, 
        ]
        sorted_by_id_data = [
        {'id':0, 'reads':0, 'likes':32, 'popularity':10},
        {'id':1, 'reads':200, 'likes':300, 'popularity':234},
        {'id':5, 'reads':100, 'likes':356, 'popularity':53}, 
        ]
        sorted_by_provider: List[Dict] = posts.results()
        self.assertEqual(sorted_by_provider, sorted_by_id_data)
    
    def test_sort_by_reads_asc(self):
        posts: Posts = Posts(direction='asc', sort_by='reads')
        posts.posts_data += [
        {'id':1, 'reads':200, 'likes':300, 'popularity':234},
        {'id':5, 'reads':100, 'likes':356, 'popularity':53}, 
        {'id':0, 'reads':0, 'likes':32, 'popularity':10},
        
        ]
        sorted_by_reads_data = [
        {'id':0, 'reads':0, 'likes':32, 'popularity':10},
        {'id':5, 'reads':100, 'likes':356, 'popularity':53}, 
        {'id':1, 'reads':200, 'likes':300, 'popularity':234},
        ]
        sorted_by_provider: List[Dict] = posts.results()
        self.assertEqual(sorted_by_provider, sorted_by_reads_data)
    
    def test_sort_by_likes_desc(self):
        posts: Posts = Posts(direction='desc', sort_by='likes')
        posts.posts_data += [
        {'id':1, 'reads':200, 'likes':300, 'popularity':234},
        {'id':5, 'reads':100, 'likes':356, 'popularity':53}, 
        {'id':0, 'reads':0, 'likes':32, 'popularity':10},
        ]
        sorted_by_likes_data = [ 
        {'id':5, 'reads':100, 'likes':356, 'popularity':53}, 
        {'id':1, 'reads':200, 'likes':300, 'popularity':234},
        {'id':0, 'reads':0, 'likes':32, 'popularity':10},
        ]
        sorted_by_provider: List[Dict] = posts.results()
        self.assertEqual(sorted_by_provider, sorted_by_likes_data)

    def test_sort_by_popularity_desc(self):
        posts: Posts = Posts(direction='desc', sort_by='popularity')
        posts.posts_data += [
        {'id':0, 'reads':0, 'likes':32, 'popularity':10},
        {'id':1, 'reads':200, 'likes':300, 'popularity':234},
        {'id':5, 'reads':100, 'likes':356, 'popularity':53}, 
        ]
        sorted_by_popularity_data = [ 
        {'id':1, 'reads':200, 'likes':300, 'popularity':234},
        {'id':5, 'reads':100, 'likes':356, 'popularity':53}, 
        {'id':0, 'reads':0, 'likes':32, 'popularity':10},
        ]
        sorted_by_provider: List[Dict] = posts.results()
        self.assertEqual(sorted_by_provider, sorted_by_popularity_data)