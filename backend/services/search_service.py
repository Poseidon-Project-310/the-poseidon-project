from typing import List, Dict, Optional
from backend.repositories.restaurant_repository import RestaurantRepository

class SearchService:
    def __init__(self, restaurant_repo: RestaurantRepository):
        self.restaurant_repo = restaurant_repo


    def browse_homepage(self) -> List[Dict]:
        """
        Feat3-FR3: User can open a restaurant's menu from the homepage.
        Returns all published restaurants with their average ratings.
        """
        all_res = self.restaurant_repo.get_all_restaurants()

        # Returns the list with average_rating and id for the UI to display
        return [res for res in all_res if res.get("is_published")]


    def get_restaurant_details(self, restaurant_id: int) -> Optional[Dict]:
        """
        Feat3-FR3: Customer reviews are visible to users.
        This "opens" the restaurant by fetching the full dictionary 
        (including menu and reviews) from the repo.
        """
        restaurant = self.restaurant_repo.get_by_id(restaurant_id)

        if restaurant and restaurant.get("is_published"):
            return restaurant
        return None
