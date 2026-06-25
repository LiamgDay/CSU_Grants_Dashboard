from decimal import Decimal
from typing import Any


def _safe_agency_name(agency: Any) -> str:
    return getattr(agency, "name", None) or "Unknown"


def _safe_cfda_text(award: Any) -> str:
    cfda_info = getattr(award, "primary_cfda_info", None) or {}
    cfda_number = cfda_info.get("cfda_number") or "Unknown"
    cfda_title = cfda_info.get("cfda_program_title") or "Unknown"
    return f"{cfda_number} - {cfda_title}"


def award_to_row(
    award: Any,
    campus_name: str,
    approved_recipient_name: str,
) -> dict[str, Any]:
    """Convert one USAspending award object into a clean dictionary row."""
    return {
        "Campus": campus_name or "Unknown",
        "Searched Recipient Name": approved_recipient_name or "Unknown",
        "Prime Award ID": award.award_identifier or "Unknown",
        "USAspending URL": award.usa_spending_url or "Unknown",
        "Recipient Name": award.recipient.name or "Unknown",
        "Recipient UEI": award.recipient.uei or "Unknown",
        "Obligations": award.total_obligation or Decimal("0.00"),
        "Outlays": award.total_outlay if award.total_outlay is not None else Decimal("0.00"),
        "Awarding Agency": _safe_agency_name(award.awarding_agency),
        "Awarding Subagency": _safe_agency_name(award.awarding_subtier_agency),
        "Period of Performance Start": award.start_date,
        "Period of Performance End": award.end_date,
        "Assisted Listing": _safe_cfda_text(award),
    }
