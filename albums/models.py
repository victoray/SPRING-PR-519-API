from typing import Optional, List

from common.models import Ownable


class Album(Ownable):
    id: str
    thumbnail: Optional[str]
    name: str
    photos: List[dict]
