from pydantic import BaseModel


class UserProduct(BaseModel):
    product_url: str
    user_id: int

class User(BaseModel):
    user_id: int
