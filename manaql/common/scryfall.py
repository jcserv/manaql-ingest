from dataclasses import dataclass
from typing import List, Optional

from dataclass_wizard import JSONListWizard


@dataclass
class Prices:
    usd: Optional[str] = None
    usd_foil: Optional[str] = None
    usd_etched: Optional[str] = None
    eur: Optional[str] = None
    eur_foil: Optional[str] = None
    tix: Optional[str] = None


@dataclass
class ImageURIs:
    small: str
    normal: str
    large: str
    png: str
    art_crop: str
    border_crop: str


@dataclass
class CardFace:
    name: str
    image_uris: Optional[ImageURIs] = None


@dataclass
class SFCard(JSONListWizard):
    name: str
    set: str
    set_name: str
    collector_number: str
    prices: Prices
    finishes: List[str]
    type_line: Optional[str] = None
    image_uris: Optional[ImageURIs] = None
    card_faces: Optional[List[CardFace]] = (
        None  # the first entry should be the front, the second should be the back
    )
