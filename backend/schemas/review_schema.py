# backend/schemas/review_schema.py
from pydantic import BaseModel, ConfigDict, Field
<<<<<<< HEAD
from datetime import datetime

# This is a dummy file to allow for review service to be tested

=======
from typing import Optional
from datetime import datetime

>>>>>>> rating_reviewing
class ReviewBase(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
<<<<<<< HEAD
        validate_assignment=True)
    rating: int = Field(..., ge=1, le=5)
=======
        validate_assignment=True
    )

    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    comment: Optional[str] = Field(default=None, max_length=1000)
>>>>>>> rating_reviewing

class ReviewCreate(ReviewBase):
    order_id: str
    restaurant_id: int
    customer_id: str
<<<<<<< HEAD
    comment: str = ""

class ReviewUpdate(BaseModel):
    rating: int
=======

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
>>>>>>> rating_reviewing

class ReviewDisplay(ReviewBase):
    id: str
    order_id: str
    customer_id: str
    restaurant_id: int
    created_at: datetime