from pydantic import BaseModel
from typing import Union
from typing import List, Literal
from dotenv import dotenv_values


#dotenv_values reads the values from the .env file and create a dictionary object
config = dotenv_values(".env")


class Connection(BaseModel):
    id: str
    title: str
    type: str


class NewRecordOne(BaseModel):
    title: str
    description: Union[str, None] = None
    content: Union[List[dict], None] = None
    visible: bool = True
    connections: Union[List[Connection], None] = None
    editors: Union[List[str], None] = None
    viewers: Union[List[str], None] = None


class RecordOne(BaseModel):
    id: str
    title: str
    description: str
    content: Union[List[dict], None] = None
    visible: bool
    owner: str
    connections: Union[List[Connection], None]
    editors: Union[List[str], None]
    viewers: Union[List[str], None]


# Record to be updated
class UpdateRecordOne(BaseModel):
    description: Union[str, None] = None
    content: Union[List[dict], None] = None
    visible: Union[bool, None] = None
    connections: Union[List[Connection], None] = None
    editors: Union[List[str], None] = None
    viewers: Union[List[str], None] = None


class UpdateRecordOneConnections(BaseModel):
    type: str  = config['RECORD_TWO_NAME']
    id: str
    operation: Literal['add', 'remove']
