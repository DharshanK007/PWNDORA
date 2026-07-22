from typing import Dict, Any, Optional

def calculate_cvss(metrics: Dict[str, Any]) -> Optional[float]:
    """
    Calculates the CVSS v3.1 base score from the given metrics dict.
    Returns None if metrics are missing or invalid.
    """
    if not metrics:
        return None

    # Constants mapping metric strings to CVSS v3.1 numerical weights
    AV_WEIGHTS = {"Network": 0.85, "Adjacent": 0.62, "Local": 0.55, "Physical": 0.20}
    AC_WEIGHTS = {"Low": 0.77, "High": 0.44}
    PR_WEIGHTS_UNCHANGED = {"None": 0.85, "Low": 0.62, "High": 0.27}
    PR_WEIGHTS_CHANGED = {"None": 0.85, "Low": 0.68, "High": 0.50}
    UI_WEIGHTS = {"None": 0.85, "Required": 0.62}
    CIA_WEIGHTS = {"High": 0.56, "Low": 0.22, "None": 0.00}

    try:
        av = AV_WEIGHTS[metrics.get("attack_vector", "Network")]
        ac = AC_WEIGHTS[metrics.get("attack_complexity", "Low")]
        scope = metrics.get("scope", "Unchanged")
        ui = UI_WEIGHTS[metrics.get("user_interaction", "None")]
        
        pr_val = metrics.get("privileges_required", "None")
        if scope == "Changed":
            pr = PR_WEIGHTS_CHANGED[pr_val]
        else:
            pr = PR_WEIGHTS_UNCHANGED[pr_val]
            
        c = CIA_WEIGHTS[metrics.get("confidentiality", "None")]
        i = CIA_WEIGHTS[metrics.get("integrity", "None")]
        a = CIA_WEIGHTS[metrics.get("availability", "None")]
    except KeyError:
        # If any metric is invalid, return None
        return None

    # Calculate Impact (ISS)
    iss = 1 - ((1 - c) * (1 - i) * (1 - a))
    
    if scope == "Unchanged":
        impact = 6.42 * iss
    else:
        impact = 7.52 * (iss - 0.029) - 3.25 * ((iss - 0.02)**15)
        
    # Calculate Exploitability
    exploitability = 8.22 * av * ac * pr * ui
    
    if impact <= 0:
        base_score = 0.0
    else:
        if scope == "Unchanged":
            base_score = min(impact + exploitability, 10.0)
        else:
            base_score = min(1.08 * (impact + exploitability), 10.0)
            
    # Round up to nearest 0.1
    return round(base_score + 0.049, 1)

