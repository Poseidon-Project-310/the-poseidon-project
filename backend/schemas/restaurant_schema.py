import uuid
from pydantic import BaseModel, PrivateAttr, ConfigDict, Field, model_validator
from typing import List, Optional

class RestaurantSchema(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True)

    # Public fields
    res_id_attr: str = Field(alias="_id") 
    name_attr: str = Field(alias="_name")
    menu_attr: List[str] = Field(default_factory=list, alias="_menu")

    owner_id_attr: Optional[str] = Field(default=None, alias="_owner_id")
    open_time_attr: Optional[int] = Field(default=None, alias="_open_time")
    close_time_attr: Optional[int] = Field(default=None, alias="_close_time")
    address_attr: Optional[str] = Field(default=None, alias="_address")
    phone_attr: Optional[str] = Field(default=None, alias="_phone")
    latitude_attr: float = Field(default=0.0, alias="_latitude")
    longitude_attr: float = Field(default=0.0, alias="_longitude")
    is_published_attr: bool = Field(default=False, alias="_is_published")

    # Private attributes
    _id: str = PrivateAttr()
    _name: str = PrivateAttr()
    _menu: List[str] = PrivateAttr(default_factory=list)

    _owner_id: Optional[str] = PrivateAttr(default=None)
    _open_time: Optional[int] = PrivateAttr(default=None)
    _close_time: Optional[int] = PrivateAttr(default=None)
    _address: Optional[str] = PrivateAttr(default=None)
    _phone: Optional[str] = PrivateAttr(default=None)
    _latitude: float = PrivateAttr(default=0.0)
    _longitude: float = PrivateAttr(default=0.0)
    _is_published: bool = PrivateAttr(default=False)

    @model_validator(mode="after")
    def validate_business_hours(self) -> "RestaurantSchema":
        # Ensure close time is after open time
        open = self.open_time_attr
        close = self.close_time_attr

        if open is not None and close is not None:
            if open >= close:
                raise ValueError("open_time must be before close_time")
        return self

    def model_post_init(self, __context):
        """
        Syncs public and private attributes
        """
        self._id = self.res_id_attr
        self._name = self.name_attr
        self._menu = self.menu_attr
        self._owner_id = self.owner_id_attr
        self._open_time = self.open_time_attr
        self._close_time = self.close_time_attr
        self._address = self.address_attr
        self._phone = self.phone_attr
        self._latitude = self.latitude_attr
        self._longitude = self.longitude_attr
        self._is_published = self.is_published_attr

    # Getters and Setters
    @property
    def restaurant_id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def menu(self) -> List[dict]:
        return self._menu
    
    @property
    def owner_id(self) -> Optional[str]:
        return self._owner_id
    
    @owner_id.setter
    def owner_id(self, value: str):
        self._owner_id = value
    
    @property
    def get_open_time(self) -> Optional[int]:
        return self._open_time
    
    @get_open_time.setter
    def get_open_time(self, value: int):
        if not (0 <= value <= 2400):
            raise ValueError("Invalid time format")
        self._open_time = value
    
    @property
    def get_close_time(self) -> Optional[int]:
        return self._close_time
    
    @get_close_time.setter
    def get_close_time(self, value: int):
        if not (0 <= value <= 2400):
            raise ValueError("Invalid time format")
        self._close_time = value
    
    @property
    def address(self) -> Optional[str]:
        return self._address
    
    @address.setter
    def address(self, value: str):
        if not value or len(value.strip()) < 5:
            raise ValueError("Address is too short or invalid")
        self._address = value
    
    @property
    def phone(self) -> Optional[str]:
        return self._phone
    
    @phone.setter
    def phone(self, value: str):
        if value and not value.replace("-", "").isdigit():
            raise ValueError("Phone number must contain only digits or hyphens")
        self._phone = value

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value
    
    @property
    def is_published(self) -> bool:
        return self._is_published
    
    @is_published.setter
    def is_published(self, value: bool):
        self._is_published = value
