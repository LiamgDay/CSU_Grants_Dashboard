import streamlit as st

from load_grants import load_grants_dataframe

if st.button("Refresh data"):
    load_grants_dataframe.clear()

df = load_grants_dataframe()
st.dataframe(
    df,
    column_config={
        "USAspending URL": st.column_config.LinkColumn(
            "Prime Award ID",
            help="Click to view in USAspending.gov",
            display_text=r".*/award/ASST_NON_([^_]+)_.*"
        ),
        "Obligations": st.column_config.NumberColumn(
            "Obligations",
            format="$%,.2f",
        ),
        "Outlays": st.column_config.NumberColumn(
            "Outlays",
            format="$%,.2f",
        ),
    },
    hide_index=True,
    column_order=[
        "USAspending URL",
        "Recipient Name",
        "Recipient UEI",
        "Obligations",
        "Outlays",
        "Awarding Agency",
        "Awarding Subagency",
        "Period of Performance Start",
        "Period of Performance End",
        "Assisted Listing",
    ],
)
