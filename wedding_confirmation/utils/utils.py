"""Utility functions for working with guest invitation data.

This module provides reusable helpers that operate on the database models,
such as functions for retrieving and normalizing invitation codes from
stored guest records.
"""

import random
import string

from sqlalchemy.orm import Session

from wedding_confirmation.db.models import Guest


def get_invitation_codes_from_db(session: Session) -> list[str]:
    """Return a normalized list of active invitation codes from the database.

    This function queries all non-null, active guest codes, normalizes them
    by trimming whitespace and converting to uppercase, removes duplicates,
    and returns the result as a sorted list of strings.

    Args:
        session: Database session used to query Guest invitation codes.

    Returns:
        A sorted list of unique, normalized invitation code strings.

    """
    result = (
        session.query(Guest.code)
        .filter(Guest.code.isnot(None))
        .filter(Guest.isActive)
        .all()
    )

    codes = {str(code).strip().upper() for (code,) in result if str(code).strip()}

    return sorted(codes)


def generate_random_id() -> str:
    """Generate a short, human-friendly random identifier.

    This function creates an identifier by combining a random name prefix with
    a four-digit numeric suffix, producing easy-to-read IDs that are still
    reasonably unique.

    Returns:
        A string containing the randomly generated identifier.

    """
    names = ["maca", "mali", "agustin", "toronja", "panque"]
    return random.choice(names) + "".join(random.choices(string.digits, k=4))
