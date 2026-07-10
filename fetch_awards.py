from datetime import date

from usaspending import USASpendingClient


MIN_USASPENDING_START_DATE = date(2007, 10, 1)


def start_date_from_year(start_year: int):
    requested_start_date = date(start_year, 1, 1)

    if requested_start_date < MIN_USASPENDING_START_DATE:
        return MIN_USASPENDING_START_DATE

    return requested_start_date


def fetch_prime_awards_for_recipient(
        client: USASpendingClient,
        recipient_search_text: str,
        award_type: str,
        limit: int | None = None,
        start_year: int | None = 2019
):
    """Perform the API call, return list of prime awards found by querying recipient_search_text"""
    #recipient_search_text seems to be similar to Filter By Keyword but only supports recipient name, UEI, or DUNS.
    query = (client.awards.search().recipient_search_text(recipient_search_text))

    if award_type == "grants":
        query = query.grants()
    elif award_type == "contracts":
        query = query.contracts()
    else:
        raise ValueError(f"Unsupported award_type: {award_type}")

    if start_year is not None:
        query = query.time_period(
            start_date=start_date_from_year(start_year),
            end_date=date.today(),
            date_type="action_date"
        )

    if limit is not None:
        query = query.limit(limit)

    return query.all()


def fetch_subawards_for_recipient(
        client: USASpendingClient,
        recipient_search_text: str,
        subaward_type: str,
        limit: int | None = None,
        start_year: int | None = 2019
):
    """Perform the API call, return list of subawards found by querying recipient_search_text"""
    #recipient_search_text seems to be similar to Filter By Keyword but only supports recipient name, UEI, or DUNS.
    query = (client.subawards.search().recipient_search_text(recipient_search_text))

    if subaward_type == "subgrants":
        query = query.grants()
    elif subaward_type == "subcontracts":
        query = query.contracts()
    else:
        raise ValueError(f"Unsupported subaward_type: {subaward_type}")

    if start_year is not None:
        query = query.time_period(
            start_date=start_date_from_year(start_year),
            end_date=date.today(),
            date_type="action_date"
        )

    if limit is not None:
        query = query.limit(limit)

    return query.all()