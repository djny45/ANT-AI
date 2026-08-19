"""Hashing helpers shared by security and ledger modules."""

import hashlib


def sha256_hex(value: str) -> str:
    """Return the hex SHA-256 digest of a string."""
    return hashlib.sha256(value.encode()).hexdigest()
