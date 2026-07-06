import pandas as pd
import streamlit as st
from usaspending import USASpendingClient

from fetch_contracts import fetch_contracts_for_recipient
from transform_contracts import contract_to_row


@st.cache_data(ttl=60 * 60 * 24, show_spinner=False)
def load_contracts_for_recipient(recipient_name: str, limit: int | None = None) -> pd.DataFrame:
    """Load the contracts for one recipient."""
    rows = []
    with USASpendingClient() as client:
        contracts = fetch_contracts_for_recipient(client, recipient_name, limit=limit)
        for contract in contracts:
            row = contract_to_row(contract)
            if row["Recipient Name"].strip().lower() == recipient_name.strip().lower():
                rows.append(row)
    return pd.DataFrame(rows)


def load_contracts_dataframe(selected_recipients: list[dict[str, str]], limit: int | None = None) -> pd.DataFrame:
    """Load contracts for selected recipients."""
    frames = []
    for recipient in selected_recipients:
        frame = load_contracts_for_recipient(recipient["name"], limit)
        if not frame.empty:
            frames.append(frame)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def clear_contracts_cache() -> None:
    """Clear cached per-recipient contract results."""
    load_contracts_for_recipient.clear()