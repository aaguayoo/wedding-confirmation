"""Integration helpers for accessing guest data stored in Google Sheets.

This module provides small utility functions for authenticating with the
Google Sheets API, selecting the configured worksheet, and reading guest
records to be used by the rest of the application.
"""

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_client() -> gspread.Client:
    """Create an authenticated Google Sheets client for the application.

    This function builds credentials from the configured service account data,
    applies the required scopes, and returns an authorized gspread client that
    can be used to access Google Sheets.

    Returns:
        An authenticated gspread Client instance configured with the
        application's service account credentials.

    """
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES,
    )
    return gspread.authorize(creds)


def get_worksheet() -> gspread.Worksheet:
    """Return a Google Sheets worksheet configured for the application.

    This function reads the spreadsheet identifier and worksheet name from
    Streamlit secrets, connects to Google Sheets using an authorized client,
    and returns the corresponding worksheet object.

    Returns:
        A gspread Worksheet instance representing the configured worksheet.

    """
    client = get_client()

    spreadsheet_id = st.secrets["google_sheets"]["spreadsheet_id"]
    worksheet_name = st.secrets["google_sheets"]["worksheet_name"]

    sh = client.open_by_key(spreadsheet_id)
    return sh.worksheet(worksheet_name)


def read_guests_from_sheet() -> list[dict]:
    """Read all guest records from the configured Google Sheets worksheet.

    This function retrieves the worksheet used to store guest data and returns
    its contents as a list of dictionaries, with each dictionary representing
    a guest row.

    Returns:
        A list of dictionaries where each item corresponds to a guest record
        read from the worksheet.

    """
    worksheet = get_worksheet()
    return worksheet.get_all_records()
