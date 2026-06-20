import streamlit as st
import pandas as pd

from usaspending import USASpendingClient

from campuses import CSU_CAMPUSES
from fetch_grants import fetch_awards_for_recipient
from transform_grants import award_to_row


all_rows = []

with USASpendingClient() as client:

    for campus in CSU_CAMPUSES:

        campus_name = campus["display_name"]

        for approved_recipient_name in campus["approved_recipient_names"]:

            awards = fetch_awards_for_recipient(
                client,
                approved_recipient_name,
            )

            for award in awards:

                row = award_to_row(
                    award,
                    campus_name,
                    approved_recipient_name
                )

                all_rows.append(row)


df = pd.DataFrame(all_rows)

st.dataframe(df)
