from pydantic import BaseModel
from typing import Union
from typing import List

class NewRecordTwo(BaseModel):
    title: str
    description: Union[str, None] = None
    content: Union[List[dict], None] = None
    visible: bool = True
    editors: Union[List[str], None] = None
    viewers: Union[List[str], None] = None

class RecordTwo(BaseModel):
    id: str
    title: str
    description: str
    content: Union[List[dict], None] = None
    visible: bool
    owner: str
    editors: Union[List[str], None]
    viewers: Union[List[str], None]

# Record to be updated
class UpdateRecordTwo(BaseModel):
    description: Union[str, None] = None
    content: Union[List[dict], None] = None
    visible: Union[bool, None] = None
    editors: Union[List[str], None] = None
    viewers: Union[List[str], None] = None
