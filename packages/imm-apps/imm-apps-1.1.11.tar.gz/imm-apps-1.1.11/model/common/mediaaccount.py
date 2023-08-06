from pydantic import BaseModel
from typing import Optional

class MediaAccount(BaseModel):
    media:str
    account:str
    password:str
    security_answer:Optional[str]
    remark:Optional[str]
    