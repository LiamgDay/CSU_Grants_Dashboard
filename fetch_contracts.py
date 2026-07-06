from usaspending import USASpendingClient


def fetch_contracts_for_recipient(client: USASpendingClient, recipient_search_text: str, limit: int | None = None):
    """Perform the API call, return list of contracts found by querying recipient_search_text"""
    query = (client.awards.search().recipient_search_text(recipient_search_text).contracts())
    if limit is not None:
        query = query.limit(limit)
    return query.all()