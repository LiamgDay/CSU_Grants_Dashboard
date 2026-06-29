from decimal import Decimal
from typing import Any
from usaspending import Award


def award_to_row(award: Award) -> dict[str, Any]:
    """Convert one USAspending award object into a clean dictionary row."""
    # The Awards are really Grants (subclasses) which is why primary_cfda_info works here despite being Grant specific.
    # When upgrading to include contracts, maybe have if Grant do primary_cfda_info, elif Contract do something else.
    return {
        "Prime Award ID": award.award_identifier or "Unknown",
        "USAspending URL": award.usa_spending_url or "Unknown",
        "Recipient Name": getattr(award.recipient, "name", None) or "Unknown",
        "Recipient UEI": getattr(award.recipient, "uei", None) or "Unknown",
        "Obligations": award.total_obligation or Decimal("0.00"),
        "Outlays": award.total_outlay or Decimal("0.00"),
        "Awarding Agency": getattr(award.awarding_agency, "name", None) or "Unknown",
        "Awarding Subagency": getattr(award.awarding_subtier_agency, "name", None) or "Unknown",
        "Period of Performance Start": award.start_date,
        "Period of Performance End": award.end_date,
        "Assisted Listing": f"{award.primary_cfda_info.get('cfda_number') or 'Unknown'} - "
                              f"{award.primary_cfda_info.get('cfda_program_title') or 'Unknown'}"
    }
