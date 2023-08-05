"""Helper utils
"""
import secrets
import string
from datetime import date, datetime, time
from typing import Any


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    raise TypeError(f"Type {type(value)} is not json-serializable")


PASSWORD_CHAR_GROUPS = (string.ascii_lowercase, string.ascii_uppercase, string.digits, "!#$.")


def generate_password(maxlen: int = 24) -> str:
    """Generate a random password conforming with Azure SQL policies.
    Resulting password's length will always be divisible by 4 and will always
    contain the same number of characters from each group."""
    if maxlen <= 0:
        raise ValueError("Max password length must be a positive integer")
    maxlen = maxlen if maxlen % 4 == 0 else maxlen + (4 - maxlen % 4)
    return "".join(
        sorted(
            (secrets.choice(group) for _ in range(int(maxlen / 4)) for group in PASSWORD_CHAR_GROUPS),
            key=lambda _: secrets.randbelow(250),
        )
    )


SIZE_CONSTRAINTS = {0: "B", 1: "kB", 2: "MB", 3: "GB", 4: "TB", 5: "PB"}


def humanize_size(sz: int):
    """Returns size in bytes humanized to units that make most sense.

    Example:
        4572564 B -> 4.57 MB

    Arguments:
        sz {int} -- Size in bytes

    Returns:
        str -- Humanized size including units
    """
    cur = sz
    num = 0
    while cur > 1000:
        cur /= 1000
        num += 1
    cur = round(cur, 2)
    return "{} {}".format(cur, SIZE_CONSTRAINTS[num])
