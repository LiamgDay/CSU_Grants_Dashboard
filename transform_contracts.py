from decimal import Decimal
from typing import Any
from usaspending import Award


def contract_to_row(contract: Award) -> dict[str, Any]:
    """Convert one USAspending contract object into a clean dictionary row."""
    # The Awards are really Contracts (subclasses) which is why contract-specific attributes work here.
    return {
        "Prime Award ID": contract.award_identifier or "Unknown",
        "USAspending URL": contract.usa_spending_url or "Unknown",
        "Recipient Name": getattr(contract.recipient, "name", None) or "Unknown",
        "Recipient UEI": getattr(contract.recipient, "uei", None) or "Unknown",
        "Obligations": contract.total_obligation or Decimal("0.00"),
        "Outlays": contract.total_outlay or Decimal("0.00"),
        "Awarding Agency": getattr(contract.awarding_agency, "name", None) or "Unknown",
        "Awarding Subagency": getattr(contract.awarding_subtier_agency, "name", None) or "Unknown",
        "Period of Performance Start": contract.start_date,
        "Period of Performance End": contract.end_date,
        "PIID": contract.piid or "Unknown",
        "Contract Award Type": contract.contract_award_type or "Unknown",
        "NAICS": f"{contract.naics_code or 'Unknown'} - "
                 f"{contract.naics_description or 'Unknown'}",
        "PSC": f"{contract.psc_code or 'Unknown'} - "
               f"{contract.psc_description or 'Unknown'}",
        "Base Exercised Options": contract.base_exercised_options or Decimal("0.00"),
        "Base and All Options": contract.base_and_all_options or Decimal("0.00")
    }