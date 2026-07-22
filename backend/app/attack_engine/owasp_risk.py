from typing import Dict, Any, Tuple

def calculate_owasp_risk(factors: Dict[str, int]) -> Tuple[float, float, str]:
    """
    Calculates the OWASP Risk Rating based on Likelihood and Impact factors.
    Returns (Likelihood Score, Impact Score, Risk Level)
    """
    # 8 Likelihood factors, defaults based on generic web app averages
    sl = factors.get("skill_level", 5)
    m = factors.get("motive", 5)
    o = factors.get("opportunity", 7)
    size = factors.get("size", 7)
    
    eod = factors.get("ease_of_discovery", 5)
    eoe = factors.get("ease_of_exploit", 5)
    aw = factors.get("awareness", 5)
    id_detect = factors.get("intrusion_detection", 5)
    
    likelihood_score = (sl + m + o + size + eod + eoe + aw + id_detect) / 8.0
    
    # 8 Impact factors, defaults
    loc = factors.get("loss_of_confidentiality", 5)
    loi = factors.get("loss_of_integrity", 5)
    loa = factors.get("loss_of_availability", 5)
    loacc = factors.get("loss_of_accountability", 5)
    
    fd = factors.get("financial_damage", 5)
    rd = factors.get("reputational_damage", 5)
    nc = factors.get("non_compliance", 5)
    pv = factors.get("privacy_violation", 5)
    
    impact_score = (loc + loi + loa + loacc + fd + rd + nc + pv) / 8.0
    
    # Map to Low/Medium/High
    def get_level(score):
        if score < 3: return "Low"
        if score < 6: return "Medium"
        return "High"
        
    ll = get_level(likelihood_score)
    il = get_level(impact_score)
    
    # Matrix calculation
    matrix = {
        ("Low", "Low"): "Minimal",
        ("Low", "Medium"): "Low",
        ("Low", "High"): "Medium",
        ("Medium", "Low"): "Low",
        ("Medium", "Medium"): "Medium",
        ("Medium", "High"): "High",
        ("High", "Low"): "Medium",
        ("High", "Medium"): "High",
        ("High", "High"): "Critical"
    }
    
    risk_level = matrix.get((ll, il), "Unknown")
    
    return likelihood_score, impact_score, risk_level
