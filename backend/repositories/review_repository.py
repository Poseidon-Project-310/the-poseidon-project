from typing import List, Dict
from backend.models.review.review_model import Review

class ReviewRepository:
    def __init__(self, db_connection):
        # Using the same shared db_connection (list or dict) as RestaurantRepo
        self.db = db_connection
        self._next_id = 1


    def add_review(self, review: Review) -> int:
        """
        Feat3-FR3: Ratings update when new reviews are added
        Saves the review data so it can be used for calculations.
        """
        review.id = self._next_id
        self._next_id += 1

        review_data = {
            "id": review.id,
            "restaurant_id": review.restaurant_id,
            "customer_id": review.customer_id,
            "customer_name": review.customer_name,
            "rating": review.rating,
            "comment": review.comment
        }

        self.db.append(review_data)
        return review.id


    def get_reviews_by_restaurant(self, restaurant_id: int) -> List[Dict]:
        """
        Feat3-FR3: Customer reviews are visible to users
        Retrieves all reviews linked to a specific restaurant.
        """
        return [r for r in self.db if r.get("restaurant_id") == restaurant_id]