from pydantic import BaseModel
from typing import Union


class NewUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

class User(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: str

# User to be updated
class UpdateUser(BaseModel):
    email: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    password: Union[str, None] = None
