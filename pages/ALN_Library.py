import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="ALN Library",
    layout="wide",
)

st.title("Assistance Listing Number Library")


@st.cache_data
def load_aln_dictionary():
    return pd.read_csv(
        "aln_dictionary.csv",
        dtype={"ALN": str},
    )


aln_df = load_aln_dictionary()

agencies = sorted(
    aln_df["Awarding Agency"]
    .dropna()
    .unique()
)


for agency in agencies:

    agency_df = aln_df[
        aln_df["Awarding Agency"] == agency
    ].copy()

    # Special hierarchical display for HHS
    if agency == "Department of Health and Human Services":

        st.header(agency)

        subagencies = sorted(
            agency_df["Awarding Subagency"]
            .dropna()
            .replace("", pd.NA)
            .dropna()
            .unique()
        )

        for subagency in subagencies:

            st.markdown(
                f"""
                <div style="
                    margin-top: 1.5rem;
                    margin-left: 2rem;
                    padding-left: 1rem;
                    border-left: 4px solid #888;
                ">
                    <h3 style="margin-bottom: 0.5rem;">
                        {subagency}
                    </h3>
                </div>
                """,
                unsafe_allow_html=True,
            )

            subagency_df = (
                agency_df[
                    agency_df["Awarding Subagency"] == subagency
                ][["ALN", "Program Name"]]
                .drop_duplicates()
                .sort_values("ALN")
                .reset_index(drop=True)
            )

            table_height = min(
                600,
                38 + (len(subagency_df) * 35)
            )

            st.dataframe(
                subagency_df,
                hide_index=True,
                use_container_width=True,
                height=table_height,
            )

    # Normal display for every other agency
    else:

        st.header(agency)

        display_df = (
            agency_df[
                ["ALN", "Program Name"]
            ]
            .drop_duplicates()
            .sort_values("ALN")
            .reset_index(drop=True)
        )

        table_height = min(
            600,
            38 + (len(display_df) * 35)
        )

        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True,
            height=table_height,
        )