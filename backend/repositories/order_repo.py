import json
import os

class OrderRepository:
    def __init__(self, file_path='backend/data/orders.json'):
        self.file_path = file_path

    def load_all(self):
        """Reads the JSON file and returns a list of dictionaries."""
        if not os.path.exists(self.file_path):
            return []
        
        with open(self.file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def save_all(self, orders):
        """Takes a list of order dictionaries and writes them to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(orders, file, indent=4)