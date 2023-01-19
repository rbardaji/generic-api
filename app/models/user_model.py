from pydantic import BaseModel

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
