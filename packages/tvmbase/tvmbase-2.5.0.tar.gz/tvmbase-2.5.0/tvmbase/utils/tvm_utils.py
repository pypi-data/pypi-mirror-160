import re

from tvmbase.constants import ADDRESS_REGEX, IDX_REGEX


def is_address(value: str) -> bool:
    return bool(re.fullmatch(ADDRESS_REGEX, value))


def is_idx(value: str) -> bool:
    return bool(re.fullmatch(IDX_REGEX, value))


def decode_bytes(value: str) -> str:
    return bytes.fromhex(value).decode()
