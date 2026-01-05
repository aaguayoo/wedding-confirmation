"""Service layer helpers for working with wedding guests.

This module centralizes common operations on the ``Guest`` model, such as
retrieving a guest by their invitation code and recording attendance
confirmation details.
"""

from sqlalchemy.orm import Session

from wedding_confirmation.db.models import Guest
from wedding_confirmation.integrations.google_sheets import (
    get_worksheet,
    read_guests_from_sheet,
)

FIELDS_FROM_SHEETS = {"Código", "Grupo", "Nombres", "Número de invitaciones", "Activo"}


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


def export_guests_to_google_sheets(session: Session) -> None:
    """Export all guests from the database to the configured Google Sheets worksheet.

    This function reads guest records from the database, transforms them into
    a tabular format with predefined headers, and writes the data into the
    worksheet so it reflects the current state of the guest list.

    Args:
        session: Database session used to query Guest records for export.

    """
    worksheet = get_worksheet()

    guests = session.query(Guest).all()

    headers = [
        "Código",
        "Grupo",
        "Nombres",
        "Número de invitaciones",
        "Confirmación",
        "Lugares confirmados",
        "Reserva Hotel de la Borda",
        "Días reservados",
        "Tipo de habitación",
        "Comentarios",
        "Activo",
    ]

    rows = [
        [
            g.code,
            g.group,
            g.names,
            g.allowed_guests,
            g.confirmation,
            g.confirmed_guests,
            g.hotel_reservation,
            g.reserved_days,
            g.reserved_room,
            g.comments,
            g.isActive,
        ]
        for g in guests
    ]

    worksheet.clear()
    worksheet.append_row(headers)  # type: ignore
    worksheet.append_rows(rows)  # type: ignore


def import_guests_from_google_sheets(session: Session) -> dict:
    """Synchronize guest records from Google Sheets into the database.

    This function reads guest rows from the configured Google Sheets worksheet,
    creates new guests or updates existing ones based on their invitation code,
    and returns a summary of how many records were created, updated, or
    skipped.

    Args:
        session: Database session used to query and persist Guest records.

    Returns:
        A dictionary with counts of created, updated, and skipped guest
        records during the import.

    """
    rows = read_guests_from_sheet()

    created = 0
    updated = 0
    deleted = 0
    skipped = 0

    def is_active(value: object) -> bool:
        """Determine whether a guest row from Google Sheets should be treated as active.

        This helper interprets different textual representations of truth
        (including localized values) and returns True when the value indicates
        the guest is active.

        Args:
            value: Raw cell value from the "Activo" column in the sheet.

        Returns:
            True

        """
        return str(value).strip().lower() in {"true", "sí", "si", "1", "yes"}

    for row in rows:
        code = str(row.get("Código", "")).strip()

        if not code:
            skipped += 1
            continue

        active = is_active(row.get("Activo", True))

        guest = session.query(Guest).filter(Guest.code == code).first()

        # 🗑️ DELETE explícito
        if not active:
            if guest:
                session.delete(guest)
                deleted += 1
            continue

        # ✏️ UPDATE
        if guest:
            for field in FIELDS_FROM_SHEETS:
                if field in row and row[field] not in ("", None):
                    setattr(guest, field, row[field])
            updated += 1

        # ➕ INSERT
        else:
            try:
                guest = Guest(
                    code=code,
                    group=row["Grupo"],
                    names=row["Nombres"],
                    allowed_guests=int(row["Número de invitaciones"]),
                    comments=row.get("Comentarios"),
                )
                session.add(guest)
                created += 1
            except KeyError:
                skipped += 1

    session.commit()

    return {
        "created": created,
        "updated": updated,
        "deleted": deleted,
        "skipped": skipped,
    }
