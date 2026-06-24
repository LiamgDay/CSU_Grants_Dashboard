import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

from load_grants import load_grants_dataframe

st.set_page_config(layout="wide")

if st.button("Refresh data"):
    load_grants_dataframe.clear()

df = load_grants_dataframe()

df["Obligations"] = df["Obligations"].astype(float)
df["Outlays"] = df["Outlays"].astype(float)

df["Period of Performance Start"] = pd.to_datetime(
    df["Period of Performance Start"]
).dt.strftime("%Y-%m-%d")

df["Period of Performance End"] = pd.to_datetime(
    df["Period of Performance End"]
).dt.strftime("%Y-%m-%d")

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
)

grid_options = gb.build()

AgGrid(
    df,
    gridOptions=grid_options,
    height=750,
    allow_unsafe_jscode=True,
    theme="streamlit",
)