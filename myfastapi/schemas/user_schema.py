from pydantic import BaseModel
from models.user_model import Users
from tortoise.contrib.pydantic import pydantic_model_creator

UserSchema = pydantic_model_creator(Users, name="User")


class UserInSchema(BaseModel):
    username: str
