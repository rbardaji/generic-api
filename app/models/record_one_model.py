from pydantic import BaseModel
from typing import Union
from typing import List


class Connection(BaseModel):
    id: str
    title: str
    type: str


class NewRecordOne(BaseModel):
    title: str
    description: Union[str, None] = None
    visible: bool = True
    connection: Union[List[Connection], None] = None
    editors: Union[List[str], None] = None
    viewers: Union[List[str], None] = None


class RecordOne(BaseModel):
    id: str
    title: str
    description: str
    visible: bool
    owner: str
    connections: Union[List[Connection], None]
    editors: Union[List[str], None]
    viewers: Union[List[str], None]


# Record to be updated
class UpdateRecordOne(BaseModel):
    description: Union[str, None] = None
    visible: Union[bool, None] = None
    connection: Union[List[Connection], None] = None
    editors: Union[List[str], None] = None
    viewers: Union[List[str], None] = None
