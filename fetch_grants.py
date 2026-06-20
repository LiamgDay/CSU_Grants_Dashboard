from typing import Any
from usaspending import USASpendingClient


def fetch_awards_for_recipient(client: USASpendingClient, recipient_name: str, limit: int | None = 5) -> list[Any]:

    query = (
        client.awards.search()
        .recipient_search_text(recipient_name)
        .grants()
    )

    if limit is not None:
        query = query.limit(limit)

    return query.all()