from typing import Any
from usaspending import USASpendingClient


def fetch_awards_for_recipient(
    client: USASpendingClient,
    recipient_search_text: str,
    limit: int | None = None,
) -> list[Any]:
    """Fetch prime grant awards for one USAspending recipient search value."""
    query = (
        client.awards.search()
        .recipient_search_text(recipient_search_text)
        .grants()
    )

    if limit is not None:
        query = query.limit(limit)

    return query.all()
