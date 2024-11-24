from dataclasses import dataclass


@dataclass
class BulkData:
    """Represents a bulk data object from Scryfall"""

    id: str
    type: str
    updated_at: str
    uri: str
    name: str
    description: str
    size: int
    download_uri: str
    content_type: str
    content_encoding: str
