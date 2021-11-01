from typing import List, Dict, Union, Set
import requests
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from requests.models import Response
from .Providers.posts import Posts


def index(request):
    return HttpResponse("Hatchway API", status=200)


def ping(request):
    if request.method == "GET":
        return JsonResponse({"success": True}, status=200)

    return HttpResponseServerError("CRUD operation is not supported",
                                   status=400)

@cache_page(60 * 15)
def posts(request):
    if request.method == "GET":
        
        tags: str = request.GET.get('tags', None)
        if tags is None:
            return HttpResponseServerError("Tags parameter is required",
                                           status=400)

        sort_by: str = request.GET.get('sortBy', 'id')
        accepted_sort_by_values: Set[str] = {'id', 'reads', 'likes', 'popularity'}
        if sort_by not in accepted_sort_by_values:
            return HttpResponseServerError("sortBy parameter is invalid",
                                           status=400)

        direction: str = request.GET.get('direction', 'asc')
        accepted_direction_values: Set[str] = {'asc', 'desc'}
        if direction not in accepted_direction_values:
            return HttpResponseServerError("direction parameter is invalid",
                                           status=400)

        tags_list: List[str] = tags.split(',')
        posts: Posts = Posts(direction=direction, sort_by=sort_by)

        for tag in tags_list:
            response: Response = \
                requests.get(
                    f"https://api.hatchways.io/assessment/blog/posts?tag={tag}")
            json_data: List[Dict[str, Union[str, int, List[str], float]]] = response.json()
            tag_posts_data: List[Dict[str, Union[str, int, List[str], float]]] = \
            json_data['posts']
            posts.posts_data += tag_posts_data

        posts_data: List[Dict[str, Union[str, int, List[str], float]]] = posts.results()

        return JsonResponse({"posts": posts_data})

    return HttpResponseServerError("CRUD operation is not supported",
                                   status=400)
