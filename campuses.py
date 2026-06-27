CSU_CAMPUSES = [
    {   
        "id": "san_luis_obispo",
        "display_name": "San Luis Obispo",
        "recipients": [
            {
                "name": "California Polytechnic State University",
                "uei": "CPVFEDRAL3U6",
            },
            {
                "name": "California Polytechnical University",
                "uei": "",
            },
            {
                "name": "Cal Poly Corporation",
                "uei": "MC4RJJM9XLT5",
            },
        ],
    },
    {
        "id": "san_diego",
        "display_name": "San Diego",
        "recipients": [
            {
                "name": "San Diego State University Foundation",
                "uei": "H59JKGFZKHL7",
            },
            {
                "name": "San Diego State University Fou",
                "uei": "",
            },
            {
                "name": "San Diego State University",
                "uei": "RN4HGABGRWV7",
            },
            {
                "name": "SDVAFA / SDSU",
                "uei": "",
            },
            {
                "name": "SDSU Growth Partnership",
                "uei": "",
            },
        ],
    },
    {
        "id": "channel_islands",
        "display_name": "Channel Islands",
        "recipients": [
            {
                "name": "California State University, Channel Islands Foundation",
                "uei": "XKLPG9DAK5J9",
            },
            {
                "name": "California State University Channel Islands",
                "uei": "RN64EPNH8JC6",
            },
        ],
    },
]
#ASSOCIATED STUDENTS INC OF CALIFORNIA POLYTECHNIC STATE UNIVERSITY AT SAN LUIS OBISPO is in subawards


def iter_recipients():
    """Yield every recipient with its parent campus metadata attached."""
    for campus in CSU_CAMPUSES:
        for recipient in campus["recipients"]:
            yield {
                "campus_id": campus["id"],
                "campus_display_name": campus["display_name"],
                **recipient,
            }


def recipient_key(campus_id: str, recipient_name: str) -> str:
    """Return a stable key for Streamlit widget/session state."""
    return f"{campus_id}::{recipient_name}"


def get_recipient_options() -> list[dict[str, str]]:
    """Return flattened recipient options used by the dashboard and loader."""
    options = []

    for recipient in iter_recipients():
        option = {
            **recipient,
            "key": recipient_key(
                recipient["campus_id"],
                recipient["name"],
            ),
        }
        options.append(option)

    return options


def get_recipients_by_key(keys: list[str] | set[str]) -> list[dict[str, str]]:
    """Resolve selected Streamlit keys back to recipient configuration objects."""
    selected_keys = set(keys)
    return [
        option
        for option in get_recipient_options()
        if option["key"] in selected_keys
    ]