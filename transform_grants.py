from typing import Any


def award_to_row(award: Any, campus_name: str, approved_recipient_name: str) -> dict[str, Any]:
    """
    Convert one USAspending award object into a clean dictionary row.
    """
    return {
        "award_id": award.award_identifier or "Unknown award ID",
        "actual_recipient_name": award.recipient.name or "Unknown recipient",
        "amount": award.total_obligation,  # Decimal
        "outlays": award.total_obligation or "Unknown outlays",
        "description": award.description or "Unknown description",
        "award_type": award.type_description or "Unknown type",
        "recipient_uei": award.recipient.uei or "Unknown UEI",
        "recipient location": str(award.recipient.location) or "Unknown location",#covers first two below
        "agency": award.awarding_agency.name or "Unknown agency",
        "awarding subagency": str(award.awarding_subtier_agency) or "Unknown subagency",
        "start_date": award.start_date,  # datetime.date
        "end_date": award.end_date,  # datetime.date


    }
    # "recipient location": award.recipient.location or "Unknown location",
    # "primary place of performance": award.primary_place_of_performance or "Unknown place of performance",


        #"campus": campus_name or "Unknown campus",
        #"approved_recipient_name": approved_recipient_name,
        #"recipient_id": award.recipient.recipient_id or "Unknown recipient ID",
        #"agency_abbreviation": award.awarding_agency.abbreviation or "Unknown agency abbreviation",
        #"agency_code": award.awarding_agency.code or "Unknown agency code",
        #"usa_spending_url": award.usa_spending_url or "Unknown usa spending URL",