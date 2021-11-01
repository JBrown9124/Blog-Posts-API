from typing import List, Dict, Union, Set
import requests
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from requests.models import Response
from .Providers.posts import Posts

# /api
def index(request):
    return HttpResponse("Hatchway API", status=200)


def ping(request):
    if request.method == "GET":
        return JsonResponse({"success": True}, status=200)

    return HttpResponseServerError("CRUD operation is not supported",
                                   status=400)
# A cache with a 15 minute timeout.
# /api/posts
@cache_page(60 * 15)
def posts(request):
    if request.method == "GET":
        
        # Check to see if they provided tags parameter.
        tags: str = request.GET.get('tags', None)
        if tags is None:
            return HttpResponseServerError("Tags parameter is required",
                                           status=400)
        
        # Check to see if they provided valid sortBy parameter.
        sort_by: str = request.GET.get('sortBy', 'id')
        accepted_sort_by_values: Set[str] = {'id', 'reads', 'likes', 'popularity'}
        if sort_by not in accepted_sort_by_values:
            return HttpResponseServerError("sortBy parameter is invalid",
                                           status=400)
        
        # Check to see if they provided valid direction parameter.
        direction: str = request.GET.get('direction', 'asc')
        accepted_direction_values: Set[str] = {'asc', 'desc'}
        if direction not in accepted_direction_values:
            return HttpResponseServerError("direction parameter is invalid",
                                           status=400)
        # Split tags values from tags parameter into a list.
        tags_list: List[str] = tags.split(',')
        # Instantiate Posts class with direction and sort_by values from query arguments.
        posts: Posts = Posts(direction=direction, sort_by=sort_by)
        
        # For every tag in our tag_list we are going to extend onto our data list in our Posts instance.
        for tag in tags_list:
            response: Response = \
                requests.get(
                    f"https://api.hatchways.io/assessment/blog/posts?tag={tag}")
            json_data: List[Dict[str, Union[str, int, List[str], float]]] = response.json()
            tag_posts_data: List[Dict[str, Union[str, int, List[str], float]]] = \
            json_data['posts']
            posts.posts_data += tag_posts_data

        # Return results method from our Posts instance.
        posts_data_results: List[Dict[str, Union[str, int, List[str], float]]] = posts.results()

        return JsonResponse({"posts": posts_data_results})

    return HttpResponseServerError("CRUD operation is not supported",
                                   status=400)
