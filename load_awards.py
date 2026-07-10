import pandas as pd
import streamlit as st
from usaspending import USASpendingClient

from fetch_awards import fetch_prime_awards_for_recipient, fetch_subawards_for_recipient
from transform_awards import award_to_row


@st.cache_data(show_spinner=False, ttl=3600)
def load_awards_for_recipient(
        recipient_name: str,
        award_type: str,
        limit: int | None = None,
        start_year: int | None = 2019
) -> pd.DataFrame:
    """Load awards for one recipient."""
    rows = []

    with USASpendingClient() as client:
        if award_type in ["grants", "contracts"]:
            awards = fetch_prime_awards_for_recipient(
                client,
                recipient_name,
                award_type,
                limit=limit,
                start_year=start_year
            )

        elif award_type in ["subgrants", "subcontracts"]:
            awards = fetch_subawards_for_recipient(
                client,
                recipient_name,
                award_type,
                limit=limit,
                start_year=start_year
            )

        else:
            raise ValueError(f"Unsupported award_type: {award_type}")

        for award in awards:
            row = award_to_row(award, award_type)

            if award_type in ["grants", "contracts"]:
                if row["Recipient Name"].strip().lower() == recipient_name.strip().lower():
                    rows.append(row)

            elif award_type in ["subgrants", "subcontracts"]:
                if row["Recipient Name"].strip().lower() == recipient_name.strip().lower():
                    rows.append(row)

    return pd.DataFrame(rows)


def load_awards_dataframe(
        selected_recipients: list[dict[str, str]],
        award_type: str,
        limit: int | None = None,
        start_year: int | None = 2019
) -> pd.DataFrame:
    """Load awards for selected recipients."""
    frames = []

    for recipient in selected_recipients:
        frame = load_awards_for_recipient(
            recipient["name"],
            award_type,
            limit=limit,
            start_year=start_year
        )

        if not frame.empty:
            frames.append(frame)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def clear_awards_cache() -> None:
    """Clear cached per-recipient award results."""
    load_awards_for_recipient.clear()