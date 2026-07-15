import pandas as pd
import streamlit as st

from usaspending import USASpendingClient

from fetch_awards import fetch_prime_awards_for_recipient, fetch_subawards_for_recipient
from transform_awards import award_to_row

import time


def names_match(row_recipient_name: str, expected_recipient_name: str) -> bool:
    """Return True when the returned award recipient name matches the expected ghost recipient name."""
    return row_recipient_name.strip().lower() == expected_recipient_name.strip().lower()


@st.cache_data(show_spinner=False)
def load_awards_for_recipient(
    recipient_name: str,
    recipient_uei: str | None,
    recipient_status: str,
    award_type: str,
    limit: int | None = None,
    start_year: int | None = 2016
) -> pd.DataFrame:
    """Load awards for one recipient.

    Active recipients search by UEI and do not require name double-checking.
    Ghost recipients search by name and still require recipient-name double-checking.
    """
    rows = []

    is_ghost = recipient_status == "ghost"
    has_uei = bool(recipient_uei and recipient_uei.strip())

    if is_ghost or not has_uei:
        search_text = recipient_name
        should_check_recipient_name = True
    else:
        search_text = recipient_uei.strip()
        should_check_recipient_name = False

    with USASpendingClient() as client:
        if award_type in ["grants", "contracts"]:
            awards = fetch_prime_awards_for_recipient(
                client,
                search_text,
                award_type,
                limit=limit,
                start_year=start_year
            )
        elif award_type in ["subgrants", "subcontracts"]:
            awards = fetch_subawards_for_recipient(
                client,
                search_text,
                award_type,
                limit=limit,
                start_year=start_year
            )
        else:
            raise ValueError(f"Unsupported award_type: {award_type}")

        for award in awards:
            row = award_to_row(award, award_type)

            if should_check_recipient_name:
                if names_match(row["Recipient Name"], recipient_name):
                    rows.append(row)
            else:
                rows.append(row)

    return pd.DataFrame(rows)


def load_awards_dataframe(
    selected_recipients: list[dict[str, str]],
    award_type: str,
    limit: int | None = None,
    start_year: int | None = 2016
) -> pd.DataFrame:
    frames = []
    progress = st.progress(0)
    status = st.empty()
    timings = []

    total = len(selected_recipients)

    for i, recipient in enumerate(selected_recipients, start=1):
        name = recipient["name"]
        uei = recipient.get("uei")
        status.write(f"Loading {i}/{total}: {name} ({uei or 'name search'})")

        start = time.perf_counter()

        try:
            frame = load_awards_for_recipient(
                recipient_name=name,
                recipient_uei=uei,
                recipient_status=recipient.get("status", "active"),
                award_type=award_type,
                limit=limit,
                start_year=start_year
            )
            elapsed = time.perf_counter() - start
            row_count = len(frame)

            timings.append({
                "recipient": name,
                "uei": uei,
                "seconds": round(elapsed, 2),
                "rows": row_count
            })

            if not frame.empty:
                frames.append(frame)

        except Exception as e:
            elapsed = time.perf_counter() - start
            timings.append({
                "recipient": name,
                "uei": uei,
                "seconds": round(elapsed, 2),
                "rows": "ERROR",
                "error": str(e)
            })
            st.warning(f"Failed on {name}: {e}")

        progress.progress(i / total)

    status.empty()
    progress.empty()

    with st.expander("Load timing"):
        st.dataframe(pd.DataFrame(timings).sort_values("seconds", ascending=False), hide_index=True)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def clear_awards_cache() -> None:
    """Clear cached per-recipient award results."""
    load_awards_for_recipient.clear()