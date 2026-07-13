from decimal import Decimal
from typing import Any

from usaspending import Award


def prime_award_to_row(award: Award, award_type: str) -> dict[str, Any]:
    """Convert one USAspending prime award object into a clean dictionary row."""
    row = {
        "Prime Award ID": award.award_identifier or "Unknown",
        "USAspending URL": award.usa_spending_url or "Unknown",
        "Recipient Name": getattr(award.recipient, "name", None) or "Unknown",
        "Recipient UEI": getattr(award.recipient, "uei", None) or "Unknown",
        "Obligations": award.total_obligation or Decimal("0.00"),
        "Outlays": award.total_outlay or Decimal("0.00"),
        "Awarding Agency": getattr(award.awarding_agency, "name", None) or "Unknown",
        "Awarding Subagency": getattr(award.awarding_subtier_agency, "name", None) or "Unknown",
        "Period of Performance Start": award.start_date,
        "Period of Performance End": award.end_date
    }

    if award_type == "grants":
        row["Assisted Listing"] = (
            f"{award.primary_cfda_info.get('cfda_number') or 'Unknown'} - "
            f"{award.primary_cfda_info.get('cfda_program_title') or 'Unknown'}"
        )

    elif award_type == "contracts":
        row["PIID"] = award.piid or "Unknown"
        row["Contract Award Type"] = award.contract_award_type or "Unknown"
        row["NAICS"] = (
            f"{award.naics_code or 'Unknown'} - "
            f"{award.naics_description or 'Unknown'}"
        )
        row["PSC"] = (
            f"{award.psc_code or 'Unknown'} - "
            f"{award.psc_description or 'Unknown'}"
        )
        row["Base Exercised Options"] = award.base_exercised_options or Decimal("0.00")
        row["Base and All Options"] = award.base_and_all_options or Decimal("0.00")

    else:
        raise ValueError(f"Unsupported award_type: {award_type}")

    return row


def subaward_to_row(subaward, award_type: str) -> dict[str, Any]:
    """Convert one USAspending subaward object into a clean dictionary row."""
    row = {
        "Sub-Award ID": subaward.sub_award_id or "Unknown",
        "Prime Award ID": subaward.prime_award_id or "Unknown",
        "Recipient Name": subaward.sub_awardee_name or "Unknown",
        "Recipient UEI": subaward.sub_recipient_uei or "Unknown",
        "Prime Recipient Name": subaward.prime_recipient_name or "Unknown",
        "Prime Recipient UEI": subaward.prime_award_recipient_uei or "Unknown",
        "Obligations": subaward.sub_award_amount or Decimal("0.00"),
        "Awarding Agency": subaward.awarding_agency or "Unknown",
        "Awarding Subagency": subaward.awarding_sub_agency or "Unknown",
        "Sub-Award Date": subaward.sub_award_date,
    }

    if award_type == "subgrants":
        assistance_listing = subaward.assistance_listing or {}

        row["Assisted Listing"] = (
            f"{assistance_listing.get('cfda_number') or 'Unknown'} - {assistance_listing.get('cfda_program_title') or 'Unkown'}"
        )

    elif award_type == "subcontracts":
        naics = subaward.naics or {}
        psc = subaward.psc or {}

        row["NAICS"] = (
            f"{naics.get('code') or 'Unkown'} - {naics.get('description') or 'Unkown'}"
        )

        row["PSC"] = (
            f"{psc.get('code') or 'Unknown'} - {psc.get('description') or 'Unknown'}"
        )

    else:
        raise ValueError(f"Unsupported award_type: {award_type}")

    return row


def award_to_row(award, award_type: str) -> dict[str, Any]:
    """Choose the correct row transform based on award type."""
    if award_type in ["grants", "contracts"]:
        return prime_award_to_row(award, award_type)

    elif award_type in ["subgrants", "subcontracts"]:
        return subaward_to_row(award, award_type)

    else:
        raise ValueError(f"Unsupported award_type: {award_type}")