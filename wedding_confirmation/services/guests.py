"""Service layer helpers for working with wedding guests.

This module centralizes common operations on the ``Guest`` model, such as
retrieving a guest by their invitation code and recording attendance
confirmation details.
"""

from sqlalchemy.orm import Session

from wedding_confirmation.db.models import Guest


def get_guest_by_code(session: Session, code: str) -> Guest | None:
    """Retrieve a guest using their unique invitation code.

    This function looks up a guest in the database whose stored code matches
    the provided value and returns that guest if found.

    Args:
        session: Database session used to perform the lookup.
        code: Invitation code used to identify the guest.

    Returns:
        The matching Guest instance if one exists, otherwise None.

    """
    return session.query(Guest).filter(Guest.code == code).first()


def confirm_attendance(
    session: Session,
    guest: Guest,
    confirmation: str,
    num_confirmed: int | None,
    comments: str,
) -> None:
    """Record the attendance confirmation details for a guest.

    This function updates the guest's confirmation status, number of confirmed
    attendees, and any accompanying comments, then persists the changes.

    Args:
        session: Database session used to persist the updated guest data.
        guest: Guest instance whose attendance information will be updated.
        confirmation: Confirmation status provided by the guest (for example,
            accepted or declined).
        num_confirmed: Number of people confirmed to attend with this guest, or
            None if not specified.
        comments: Additional comments or notes supplied along with the
            confirmation.

    """
    guest.confirmation = confirmation
    guest.confirmed_guests = num_confirmed
    guest.comments = comments
    session.commit()
