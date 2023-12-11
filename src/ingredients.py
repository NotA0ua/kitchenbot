from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str
    eng: str
    emoji: str = Field(max_length=1)
    uid: int


class Inventory(BaseModel):
    tomato: Ingredient = Ingredient(name="томат", eng="tomato", emoji="🍅", uid=1)
    cucumber: Ingredient = Ingredient(name="огурец", eng="cucumber", emoji="🥒", uid=2)
    egg: Ingredient = Ingredient(name="яйцо", eng="egg", emoji="🥚", uid=3)
    
