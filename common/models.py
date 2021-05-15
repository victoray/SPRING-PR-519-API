from typing import Optional

from pydantic import BaseModel


class Ownable(BaseModel):
    userId: Optional[str]
