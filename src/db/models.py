from beanie import Document, Indexed

from src.ingredients import Inventory

class User(Document):
    user_id: Indexed(int, unique=True)
    inventory: Inventory = Inventory()
