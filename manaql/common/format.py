from enum import Enum
from typing import Dict, List

from django.core.exceptions import ValidationError
from django.db import models


class Format(str, Enum):
    """Magic: The Gathering formats as defined by Scryfall."""

    STANDARD = "standard"
    FUTURE = "future"
    HISTORIC = "historic"
    TIMELESS = "timeless"
    GLADIATOR = "gladiator"
    PIONEER = "pioneer"
    EXPLORER = "explorer"
    MODERN = "modern"
    LEGACY = "legacy"
    PAUPER = "pauper"
    VINTAGE = "vintage"
    PENNY = "penny"
    COMMANDER = "commander"
    OATHBREAKER = "oathbreaker"
    STANDARDBRAWL = "standardbrawl"
    BRAWL = "brawl"
    ALCHEMY = "alchemy"
    PAUPERCOMMANDER = "paupercommander"
    DUEL = "duel"
    OLDSCHOOL = "oldschool"
    PREMODERN = "premodern"
    PREDH = "predh"

    @classmethod
    def choices(cls) -> List[tuple]:
        """Return choices for Django model field."""
        return [(format.value, format.value) for format in cls]


class LegalityStatus(str, Enum):
    """Legal status values from Scryfall."""

    LEGAL = "legal"
    NOT_LEGAL = "not_legal"
    BANNED = "banned"
    RESTRICTED = "restricted"


class FormatLegalities:
    """Efficient encoding for Magic: The Gathering format legalities.

    Uses 2 bits per format to encode all 4 possible states:
    - 00: not_legal (default)
    - 01: legal
    - 10: banned
    - 11: restricted

    For 22 formats, this requires 44 bits, which fits in a 64-bit integer.
    """

    # 2-bit masks for each format (2 bits per format)
    FORMAT_BITS = {
        Format.STANDARD: (0, 1),  # bits 0-1
        Format.FUTURE: (2, 3),  # bits 2-3
        Format.HISTORIC: (4, 5),  # bits 4-5
        Format.TIMELESS: (6, 7),  # bits 6-7
        Format.GLADIATOR: (8, 9),  # bits 8-9
        Format.PIONEER: (10, 11),  # bits 10-11
        Format.EXPLORER: (12, 13),  # bits 12-13
        Format.MODERN: (14, 15),  # bits 14-15
        Format.LEGACY: (16, 17),  # bits 16-17
        Format.PAUPER: (18, 19),  # bits 18-19
        Format.VINTAGE: (20, 21),  # bits 20-21
        Format.PENNY: (22, 23),  # bits 22-23
        Format.COMMANDER: (24, 25),  # bits 24-25
        Format.OATHBREAKER: (26, 27),  # bits 26-27
        Format.STANDARDBRAWL: (28, 29),  # bits 28-29
        Format.BRAWL: (30, 31),  # bits 30-31
        Format.ALCHEMY: (32, 33),  # bits 32-33
        Format.PAUPERCOMMANDER: (34, 35),  # bits 34-35
        Format.DUEL: (36, 37),  # bits 36-37
        Format.OLDSCHOOL: (38, 39),  # bits 38-39
        Format.PREMODERN: (40, 41),  # bits 40-41
        Format.PREDH: (42, 43),  # bits 42-43
    }

    # Status encoding (2 bits)
    STATUS_ENCODING = {
        LegalityStatus.NOT_LEGAL: 0,  # 00
        LegalityStatus.LEGAL: 1,  # 01
        LegalityStatus.BANNED: 2,  # 10
        LegalityStatus.RESTRICTED: 3,  # 11
    }

    # Reverse mapping for decoding
    ENCODING_TO_STATUS = {v: k for k, v in STATUS_ENCODING.items()}

    @classmethod
    def from_legalities(cls, legalities: Dict[str, str]) -> int:
        """Convert Scryfall legalities dict to encoded integer.

        Args:
            legalities: Dict mapping format names to legality status

        Returns:
            Integer encoding all format legalities (44 bits)
        """
        encoded = 0

        for format_name, status in legalities.items():
            try:
                format_enum = Format(format_name)
                if format_enum in cls.FORMAT_BITS:
                    bit_start, bit_end = cls.FORMAT_BITS[format_enum]
                    status_enum = LegalityStatus(status)
                    status_value = cls.STATUS_ENCODING[status_enum]

                    # Clear the 2 bits for this format and set the new value
                    mask = 3 << bit_start  # 3 = 0b11, clears 2 bits
                    encoded = (encoded & ~mask) | (status_value << bit_start)
            except (ValueError, KeyError):
                continue

        return encoded

    @classmethod
    def to_legalities(cls, encoded: int) -> Dict[str, str]:
        """Convert encoded integer back to legalities dict.

        Args:
            encoded: Integer encoding all format legalities

        Returns:
            Dict mapping format names to legality status
        """
        legalities = {}

        for format_enum, (bit_start, bit_end) in cls.FORMAT_BITS.items():
            # Extract 2 bits for this format
            status_value = (encoded >> bit_start) & 3  # 3 = 0b11
            status_enum = cls.ENCODING_TO_STATUS[status_value]
            legalities[format_enum.value] = status_enum.value

        return legalities

    @classmethod
    def get_status(cls, encoded: int, format_name: str) -> str:
        """Get legality status for a specific format.

        Args:
            encoded: Integer encoding all format legalities
            format_name: Name of the format to check

        Returns:
            Legality status as string
        """
        try:
            format_enum = Format(format_name)
            if format_enum in cls.FORMAT_BITS:
                bit_start, bit_end = cls.FORMAT_BITS[format_enum]
                status_value = (encoded >> bit_start) & 3
                status_enum = cls.ENCODING_TO_STATUS[status_value]
                return status_enum.value
        except (ValueError, KeyError):
            pass

        return LegalityStatus.NOT_LEGAL.value


class LegalitiesField(models.Field):
    """
    Custom Django field for storing format legalities in optimized space.

    Uses 6 bytes to store 44 bits (22 formats × 2 bits each).
    This is more space-efficient than BigIntegerField (8 bytes).
    """

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 6  # 6 bytes
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        if connection.vendor == "postgresql":
            return "BYTEA"  # PostgreSQL binary field
        else:
            return "BINARY(6)"  # MySQL binary field

    def from_db_value(self, value, expression, connection):
        if value is None:
            return 0
        # Convert 6-byte binary to integer
        return int.from_bytes(value, byteorder="big")

    def to_python(self, value):
        if isinstance(value, int):
            return value
        if value is None:
            return 0
        return int(value)

    def get_prep_value(self, value):
        if value is None:
            value = 0
        # Convert integer to 6-byte binary
        return value.to_bytes(6, byteorder="big")

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value < 0:
            raise ValidationError("Legalities value cannot be negative")
        if value > (1 << 44) - 1:  # Max value for 44 bits
            raise ValidationError("Legalities value exceeds maximum allowed")
