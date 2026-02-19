# backend/models/user/roles.py
#this file defines the different user roles in the system

#user roles as constants
CUSTOMER = "customer"
RESTAURANT_OWNER = "restaurant_owner"
ADMIN = "admin"

#set of all roles for easy validation
ALL_ROLES = {CUSTOMER, RESTAURANT_OWNER, ADMIN}
