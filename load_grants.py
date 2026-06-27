import pandas as pd
import streamlit as st
from usaspending import USASpendingClient

from fetch_grants import fetch_awards_for_recipient
from transform_grants import award_to_row


@st.cache_data(ttl=60 * 60 * 24, show_spinner=False)
def load_grants_for_recipient(recipient_name: str, limit: int | None = None) -> pd.DataFrame:
    """Load the grants for one recipient."""
    rows = []
    with USASpendingClient() as client:
        awards = fetch_awards_for_recipient(client, recipient_name, limit=limit)
        for award in awards:
            row = award_to_row(award)
            if row["Recipient Name"].strip().lower() == recipient_name.strip().lower():
                rows.append(row)
    return pd.DataFrame(rows)


def load_grants_dataframe(selected_recipients: list[dict[str, str]],limit: int | None = None) -> pd.DataFrame:
    """Load grants for selected recipients."""
    frames = []
    for recipient in selected_recipients: # Check how it is used in dashboard.py
        frame = load_grants_for_recipient(recipient["name"], limit)
        if not frame.empty:
            frames.append(frame)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def clear_grants_cache() -> None:
    """Clear cached per-recipient grant results."""
    load_grants_for_recipient.clear()
