import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

from campuses import CSU_CAMPUSES, get_recipient_options, get_recipients_by_key, recipient_key
from load_grants import clear_grants_cache, load_grants_dataframe

st.set_page_config(layout="wide")
st.title("CSU Grants Dashboard")

recipient_options = get_recipient_options()
all_recipient_keys = [option["key"] for option in recipient_options]

if "active_recipient_keys" not in st.session_state:
    st.session_state["active_recipient_keys"] = []

with st.sidebar:
    st.header("Grant Search")

    select_all = st.checkbox("All CSUs", value=False)
    selected_keys = set(all_recipient_keys if select_all else [])

    st.caption("Checking a campus selects every recipient currently mapped under it. Expand a campus to select individual recipients.")

    for campus in CSU_CAMPUSES:
        campus_recipients = campus["recipients"]
        campus_keys = [
            recipient_key(campus["id"], recipient["name"])
            for recipient in campus_recipients
        ]

        campus_checked = st.checkbox(
            campus["display_name"],
            value=select_all,
            key=f"campus_{campus['id']}",
            disabled=select_all,
        )

        if campus_checked:
            selected_keys.update(campus_keys)

        with st.expander(f"{campus['display_name']} recipients"):
            for recipient in campus_recipients:
                key = recipient_key(campus["id"], recipient["name"])
                recipient_checked = st.checkbox(
                    recipient["name"],
                    value=select_all or campus_checked,
                    key=f"recipient_{key}",
                    disabled=select_all or campus_checked,
                )

                if recipient_checked:
                    selected_keys.add(key)

    st.divider()

    fetch_all_awards = st.checkbox("Fetch all matching awards", value=True)
    award_limit = None

    if not fetch_all_awards:
        award_limit = st.number_input(
            "Development award limit per recipient",
            min_value=1,
            max_value=1000,
            value=5,
            step=1,
        )

    if st.button("Load selected grants", type="primary"):
        st.session_state["active_recipient_keys"] = sorted(selected_keys)

    if st.button("Refresh cached data"):
        clear_grants_cache()
        st.session_state["active_recipient_keys"] = sorted(selected_keys)
        st.success("Cached grant data cleared.")

selected_recipients = get_recipients_by_key(st.session_state["active_recipient_keys"])

if not selected_recipients:
    st.info("Select one or more campuses or recipients, then click Load selected grants.")
    st.stop()

with st.spinner("Loading selected grant data..."):
    df = load_grants_dataframe(selected_recipients, limit=award_limit)

if df.empty:
    st.warning("No grant awards were returned for the selected recipients.")
    st.stop()

st.caption(
    f"Showing {len(df):,} awards from {len(selected_recipients):,} selected recipient name(s)."
)

df["Obligations"] = pd.to_numeric(df["Obligations"])
df["Outlays"] = pd.to_numeric(df["Outlays"])

for column in ["Period of Performance Start", "Period of Performance End"]:
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors="coerce").dt.strftime("%Y-%m-%d")

gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_default_column(
    filter=True,
    sortable=True,
    resizable=True,
    floatingFilter=True,
    wrapText=True,
    autoHeight=True,
    minWidth=160,
)

gb.configure_column("Recipient Name", minWidth=260)
gb.configure_column("Awarding Agency", minWidth=220)
gb.configure_column("Awarding Subagency", minWidth=260)
gb.configure_column("Assisted Listing", minWidth=420)

gb.configure_column(
    "Obligations",
    type=["numericColumn"],
    valueFormatter="x.toLocaleString('en-US', {style: 'currency', currency: 'USD'})",
)

gb.configure_column(
    "Outlays",
    type=["numericColumn"],
    valueFormatter="x.toLocaleString('en-US', {style: 'currency', currency: 'USD'})",
)

prime_award_link_renderer = JsCode("""
class PrimeAwardLinkRenderer {
    init(params) {
        const url = params.data["USAspending URL"];
        const awardId = params.data["Prime Award ID"];

        this.eGui = document.createElement('a');
        this.eGui.innerText = awardId;
        this.eGui.setAttribute('href', url);
        this.eGui.setAttribute('target', '_blank');
        this.eGui.setAttribute('rel', 'noopener noreferrer');
    }

    getGui() {
        return this.eGui;
    }
}
""")

gb.configure_column(
    "Prime Award ID",
    header_name="Prime Award ID",
    cellRenderer=prime_award_link_renderer,
    minWidth=220,
)

gb.configure_column(
    "USAspending URL",
    hide=True,
)

gb.configure_grid_options(
    rowHeight=72,
    headerHeight=42,
    floatingFiltersHeight=36,
    domLayout="normal",
    pagination=True,
    paginationPageSize=25,
)


grid_options = gb.build()

AgGrid(
    df,
    gridOptions=grid_options,
    height=750,
    allow_unsafe_jscode=True,
    theme="streamlit",
)
