Search service test documentation

<img width="597" height="133" alt="Screenshot 2026-04-02 at 7 48 28 PM" src="https://github.com/user-attachments/assets/7d932db5-6252-433f-b1ae-c7ab93966c95" />

We have functional tests to test browsing homepage and ensure it only returns published and another tests to get restaurant details.

We have edge case tests to try to get restaurant details of an unpublished restaurant, get details of a nonexistent restaurant, and tests that homepage does not crash if no restaurants are published.

There is three more home page tests,
One tests to ensure it will filter out unpublished on the home page.
Another test ensures you can successfully get restaurant details from home.
Another test ensures tries to get info of a restaurant that isnt found or hidden.

There are two tests for pagination.
One test tests the boundaries using BVA to ensure the limit of 20 works
The next one is purely functional to ensure total pages are correctly calculated and everything runs smoothly
