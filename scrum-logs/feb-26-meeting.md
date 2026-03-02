Feb 26 meeting

Attendance in labs
- Brady wants people to be there when possible.

Need to reformat how we are doing PRs
- Base it on FRs - reformat things
- Order and Cart remain separate because user can only have one cart but can place multiple orders
- merge fulfillment request and order status
- Should open/cosed be an attribute -> Grayson do research on if time can trigger
- Admin - modify email/credentials
- Leave viewAllOrders to the end
- Restructure how we do things
- Try and make your past PRs relate to a FR - or try to in the future
- ⁠** Make all User, Customer, Restaurant attributes private - add underscore
- Delegated tasks
- Grayson will make a note of it on documents
- Services vs Routes : Do some research


Brady's talking points: (REFER TO UPPER NOTES FIRST FOR GROUP CONSENSUS)
•⁠  ⁠ALL PR’s MUST BE ASSOCIATED WITH FR’s, WE ARE DOING IT WRONG
•⁠  ⁠MenuItem: change availability to isAvailable (since it is boolean)
•⁠  ⁠Customer: remove adding to cart methods, instead assign an Order object to Customer
•⁠  ⁠Merge Cart and Order
•⁠  ⁠FulfillmentRequest be removed from CD and just incorporate that into OrderStatus (ie. Pending, Ready)
•⁠  ⁠Repositories need to be added to CD and activities, like log in etc
•⁠  ⁠Restaurant.is_open… should be replaced with a method that tells you if it’s open or not based on current time (since is open should not have to be modified by restaurant owner)
•⁠  ⁠Update Admin.modify_credentials to be able to modify email as well 
•⁠  ⁠Admin.viewAllOrders()… work on later, however in CD don’t need Admin.viewAllRequests() since you could just pass view all orders and sort by Order Status: Pending
•⁠  ⁠Admin idea: instead of current implementation, view_flagged_reviews()
•⁠  ⁠** Make all User, Customer, Restaurant attributes private

Action Items
Everyone:
- try and adjust your PRs to fall under a FR
- Start working on your Feature FRs that are in the 'in progress' tab
- Make adjustments as needed to things mentioned in scrum meeting
- Research service vs routes
Brady:
- Work on adjusting class diagram
Grayson:
- Create distribution plan on shared document
