from typing import List

from pymongo.cursor import Cursor


def photos_to_dict(result: Cursor) -> List[dict]:
    photos = []
    for doc in result:
        doc.pop("_id")
        photos.append(doc)

    return photos
