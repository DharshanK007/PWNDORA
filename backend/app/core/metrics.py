def calculate_cvss_v3_1(cvss_dict: dict) -> float:
    # A simple mock calculation for CVSS
    return 7.5

def get_owasp_risk_rating(likelihood: int, impact: int) -> str:
    avg = (likelihood + impact) / 2.0
    if avg < 3:
        return "Low"
    elif avg < 6:
        return "Medium"
    elif avg < 8:
        return "High"
    else:
        return "Critical"
