import pandas as pd
import streamlit as st
from usaspending import USASpendingClient

from fetch_grants import fetch_awards_for_recipient
from transform_grants import award_to_row


@st.cache_data(ttl=60 * 60 * 24, show_spinner=False)
def load_grants_for_recipient(
    campus_name: str,
    recipient_name: str,
    uei: str = "",
    limit: int | None = None,
) -> pd.DataFrame:
    """Load and cache grants for one recipient.

    The cache is intentionally per recipient so selecting one campus at a time
    builds reusable cached results for a later "all campuses" selection.
    """
    query_value = uei.strip() or recipient_name
    rows = []

    with USASpendingClient() as client:
        awards = fetch_awards_for_recipient(client, query_value, limit=limit)

        for award in awards:
            rows.append(
                award_to_row(
                    award,
                    campus_name,
                    recipient_name,
                )
            )

    return pd.DataFrame(rows)


def load_grants_dataframe(
    selected_recipients: list[dict[str, str]],
    limit: int | None = None,
) -> pd.DataFrame:
    """Load grants for selected recipients and combine them into one dataframe."""
    frames = []

    for recipient in selected_recipients:
        frame = load_grants_for_recipient(
            campus_name=recipient["campus_display_name"],
            recipient_name=recipient["name"],
            uei=recipient.get("uei", ""),
            limit=limit,
        )

        if not frame.empty:
            frames.append(frame)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def clear_grants_cache() -> None:
    """Clear cached per-recipient grant results."""
    load_grants_for_recipient.clear()
