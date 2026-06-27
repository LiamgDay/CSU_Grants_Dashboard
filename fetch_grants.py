from usaspending import USASpendingClient


def fetch_awards_for_recipient(client: USASpendingClient, recipient_search_text: str, limit: int | None = None):
    """Perform the API call, return list of awards found by querying recipient_search_text"""
    #recipient_search_text seems to be similar to Filter By Keyword but only supports recipient name, UEI, or DUNS.
    query = (client.awards.search().recipient_search_text(recipient_search_text).grants())
    if limit is not None:
        query = query.limit(limit)
    return query.all()
