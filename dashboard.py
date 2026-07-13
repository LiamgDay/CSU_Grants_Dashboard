import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from datetime import date

from campuses import CSU_CAMPUSES, get_recipient_options, get_recipients_by_key, recipient_key
from load_awards import clear_awards_cache, load_awards_dataframe


AWARD_TYPES = ["grants", "contracts", "subgrants", "subcontracts"]


st.set_page_config(layout="wide")
st.title("CSU Awards Dashboard")

recipient_options = get_recipient_options()
active_recipient_options = [
    option for option in recipient_options
    if option.get("status", "active") != "ghost"
]
ghost_recipient_options = [
    option for option in recipient_options
    if option.get("status") == "ghost"
]

all_active_recipient_keys = [option["key"] for option in active_recipient_options]
all_ghost_recipient_keys = [option["key"] for option in ghost_recipient_options]


if "active_recipient_keys" not in st.session_state:
    st.session_state["active_recipient_keys"] = []

if "active_award_type" not in st.session_state:
    st.session_state["active_award_type"] = "grants"

with st.sidebar:
    st.header("Award Search")

    award_type = st.selectbox(
        "Award Type",
        AWARD_TYPES,
        index=AWARD_TYPES.index(st.session_state["active_award_type"])
    )

    select_all = st.checkbox("All CSUs", value=False)

    selected_ghost_keys = st.multiselect(
        "Ghost recipients to include",
        options=all_ghost_recipient_keys,
        format_func=lambda key: next(
            f"{option['campus_display_name']} — {option['name']}"
            for option in ghost_recipient_options
            if option["key"] == key
        ),
        help="Use this for discontinued names, typos, or one-off USAspending recipient names.",
    )

    selected_keys = set(all_active_recipient_keys if select_all else [])
    selected_keys.update(selected_ghost_keys)

    

    for campus in CSU_CAMPUSES:
        campus_recipients = campus["recipients"]
        active_campus_recipients = [
            recipient for recipient in campus_recipients
            if recipient.get("status", "active") != "ghost"
        ]
        campus_keys = [
            recipient_key(campus["id"], recipient["name"])
            for recipient in active_campus_recipients
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
            for recipient in active_campus_recipients:
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

    no_time_restriction = st.checkbox("No time restriction", value=False)
    start_year = None

    if not no_time_restriction:
        start_year = st.number_input(
            "Load awards from year",
            min_value=2007,
            max_value=date.today().year,
            value=2019,
            step=1
        )

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

    if st.button("Load selected awards", type="primary"):
        st.session_state["active_recipient_keys"] = sorted(selected_keys)
        st.session_state["active_award_type"] = award_type

    if st.button("Refresh cached data"):
        clear_awards_cache()

        st.session_state["active_recipient_keys"] = sorted(selected_keys)
        st.session_state["active_award_type"] = award_type
        st.success(f"Cached {award_type} data cleared.")

selected_recipients = get_recipients_by_key(st.session_state["active_recipient_keys"])
active_award_type = st.session_state["active_award_type"]

if not selected_recipients:
    st.info("Select one or more campuses or recipients, then click Load selected awards.")
    st.stop()

with st.spinner(f"Loading selected {active_award_type} data..."):
    df = load_awards_dataframe(
        selected_recipients,
        active_award_type,
        limit=award_limit,
        start_year=start_year
    )

if df.empty:
    st.warning(f"No {active_award_type} were returned for the selected recipients.")
    st.stop()

st.caption(
    f"Showing {len(df):,} {active_award_type} from {len(selected_recipients):,} selected recipient name(s)."
)

@st.cache_data
def convert_df_to_csv(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")

csv = convert_df_to_csv(df)

st.download_button(
    label="Download results as CSV",
    data=csv,
    file_name=f"csu_{active_award_type}_awards.csv",
    mime="text/csv",
)

money_columns = [
    "Obligations",
    "Outlays",
    "Base Exercised Options",
    "Base and All Options",
]

for column in money_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column])

metric_cols = st.columns(len([col for col in money_columns if col in df.columns]))

for metric_col, column in zip(metric_cols, [col for col in money_columns if col in df.columns]):
    total = df[column].sum()

    metric_col.metric(
        label=f"Total {column}",
        value=f"${total:,.0f}"
    )

date_columns = [
    "Period of Performance Start",
    "Period of Performance End",
    "Sub-Award Date"
]

for column in date_columns:
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

if "Prime Recipient Name" in df.columns:
    gb.configure_column("Prime Recipient Name", minWidth=260)

if "Assisted Listing" in df.columns:
    gb.configure_column("Assisted Listing", minWidth=420)

if "NAICS" in df.columns:
    gb.configure_column("NAICS", minWidth=420)

if "PSC" in df.columns:
    gb.configure_column("PSC", minWidth=420)

for column in money_columns:
    if column in df.columns:
        gb.configure_column(
            column,
            type=["numericColumn"],
            valueFormatter="x.toLocaleString('en-US', {style: 'currency', currency: 'USD'})",
        )

prime_award_link_renderer = JsCode("""
class PrimeAwardLinkRenderer {
    init(params) {
        const url = params.data["USAspending URL"];
        const awardId = params.data["Prime Award ID"];

        this.eGui = document.createElement(url ? 'a' : 'span');
        this.eGui.innerText = awardId;

        if (url) {
            this.eGui.setAttribute('href', url);
            this.eGui.setAttribute('target', '_blank');
            this.eGui.setAttribute('rel', 'noopener noreferrer');
        }
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

if "USAspending URL" in df.columns:
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