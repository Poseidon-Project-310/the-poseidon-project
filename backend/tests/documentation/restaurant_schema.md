Test documentation for restaurant_schema

<img width="585" height="128" alt="Screenshot 2026-03-22 at 10 39 59 AM" src="https://github.com/user-attachments/assets/147e66e9-05cb-48bd-b3c2-dc94786bffe3" />

The schema initialization test uses equivalence partitioning and maps the data from the fixture to private attributes

The optional null fields test uses equivalence partitioning and tests that the optional tests when empty doesn't cause an error

The encapsulation boundaries test uses fault injection and tries to access a protected attribute

The invalid time logic test uses exception handling and tests handling invalid date and throws error through the setters

The invalid time relationship uses exception handling and ensures that open time cannot be after or equal to close time

The restaurant serialization test uses mocking to ensure you are able to save through the repository

The status update test is a positive functional test and tests the data flow to publish restaurants

The restaurant to private mapping test is a positive functional test that matches public fields to post_init
