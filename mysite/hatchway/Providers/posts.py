from operator import itemgetter
from typing import List, Dict, Union


class Posts(object):
    
    def __init__(self, sort_by: str = "id", direction: str = "asc"):
        
        self.sort_by: str = sort_by
        self.direction: str = direction
        self.posts_data: List[Dict[str, Union[str, int, List[str], float]]] = []
    
    # Remove all duplicates from our posts data based on post "id".
    def remove_duplicates(self) -> List[
        Dict[str, Union[str, int, List[str], float]]]:
        
        
        no_duplicates_posts_data: List[
            Dict[str, Union[str, int, List[str], float]]] = \
            list({v['id']: v for v in self.posts_data}.values())
        
        return no_duplicates_posts_data
    
    # Sort by given sort_by and reverse based on given direction.
    def sort_by_value(self) -> List[
        Dict[str, Union[str, int, List[str], float]]]:
        
        no_duplicates_posts_data: List[
            Dict[str, Union[
                str, int, List[str], float]]] = self.remove_duplicates()
        
        sorted_posts_data: List[
            Dict[str, Union[str, int, List[str], float]]] = sorted(
            no_duplicates_posts_data,
            key=itemgetter(self.sort_by),
            reverse=(
                    self.direction ==
                    "desc"))
        
        return sorted_posts_data

    def results(self) -> List[Dict[str, Union[str, int, List[str], float]]]:
        
        posts_data: List[
            Dict[str, Union[str, int, List[str], float]]] = self.sort_by_value()
        
        return posts_data
