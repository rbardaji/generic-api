from pydantic import BaseModel
from typing import Union
from typing import List

class NewRecordOne(BaseModel):
    title: str
    description: Union[str, None] = None
    visible: bool = True
    editors: Union[List[str], None] = None
    viewers: Union[List[str], None] = None

class RecordOne(BaseModel):
    id: str
    title: str
    description: str
    visible: bool
    owner: str
    editors: Union[List[str], None]
    viewers: Union[List[str], None]

# Record to be updated
class UpdateRecordOne(BaseModel):
    description: Union[str, None] = None
    visible: Union[bool, None] = None
    editors: Union[List[str], None] = None
    viewers: Union[List[str], None] = None
