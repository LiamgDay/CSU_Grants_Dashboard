from typing import Any


def award_to_row(award: Any, campus_name: str, approved_recipient_name: str) -> dict[str, Any]:
    """
    Convert one USAspending award object into a clean dictionary row.
    """
    return {
        "Prime Award ID": award.award_identifier or "Unknown", #use if the url system isn't working
        "USAspending URL": award.usa_spending_url or "Unknown",
        "Recipient Name": award.recipient.name or "Unknown", #good
        "Recipient UEI": award.recipient.uei or "Unknown", #good
        "Obligations": award.total_obligation or "Unknown",  # Decimal #good
        "Outlays": award.total_obligation or "Unknown", #good
        "Awarding Agency": award.awarding_agency.name or "Unknown", #good
        "Awarding Subagency": award.awarding_subtier_agency.name or "Unknown", #check
        "Period of Performance Start": award.start_date,  # datetime.date
        "Period of Performance End": award.end_date,  # datetime.date
        "Assisted Listing": f"{award.primary_cfda_info['cfda_number']} - {award.primary_cfda_info['cfda_program_title']}" or "Unknown"
    }
    #: str(award.recipient.location) or "Unknown location",  # covers first two below
    # "recipient location": award.recipient.location or "Unknown location",
    # "primary place of performance": award.primary_place_of_performance or "Unknown place of performance",

        #"award_type": award.type_description or "Unknown type",
        #"campus": campus_name or "Unknown campus",
        #"approved_recipient_name": approved_recipient_name,
        #"recipient_id": award.recipient.recipient_id or "Unknown recipient ID",
        #"agency_abbreviation": award.awarding_agency.abbreviation or "Unknown agency abbreviation",
        #"agency_code": award.awarding_agency.code or "Unknown agency code",
        #"usa_spending_url": award.usa_spending_url or "Unknown usa spending URL",
        #"description": award.description or "Unknown description",