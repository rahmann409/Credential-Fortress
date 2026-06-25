# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import math
from typing import List, Dict, Any

def calculate_entropy(password: str) -> float:
    """Calculates the Shannon entropy estimate of the password."""
    if not password:
        return 0.0
        
    charset_size = 0
    if any(c.islower() for c in password): charset_size += 26
    if any(c.isupper() for c in password): charset_size += 26
    if any(c.isdigit() for c in password): charset_size += 10
    if not password.isalnum(): charset_size += 32
    
    if charset_size == 0:
        return 0.0
        
    return len(password) * math.log2(charset_size)

def evaluate_strength(password: str, dictionary: List[str]) -> Dict[str, Any]:
    """Evaluates password strength and checks dictionary overlap."""
    entropy = calculate_entropy(password)
    length = len(password)
    in_dictionary = password.lower() in [w.lower() for w in dictionary]
    
    score = 0
    if length >= 12: score += 1
    if entropy >= 50: score += 1
    if not in_dictionary: score += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c.isdigit() for c in password) and not password.isalnum():
        score += 1
        
    if in_dictionary:
        status = "Weak (Dictionary overlap)"
    elif score >= 4:
        status = "Strong"
    elif score >= 2:
        status = "Moderate"
    else:
        status = "Weak"
        
    suggestions = []
    if length < 12:
        suggestions.append("Increase length to at least 12 characters.")
    if in_dictionary:
        suggestions.append("Avoid common words or patterns found in dictionaries.")
    if entropy < 50:
        suggestions.append("Increase complexity by mixing character types.")
        
    return {
        "password": password,
        "length": length,
        "entropy": round(entropy, 2),
        "in_dictionary": in_dictionary,
        "status": status,
        "suggestions": suggestions
    }

def analyze_dataset(passwords: List[str], dictionary: List[str]) -> List[Dict[str, Any]]:
    """Analyzes a list of synthetic passwords against a dictionary."""
    results = []
    seen = set()
    for pwd in passwords:
        res = evaluate_strength(pwd, dictionary)
        if pwd in seen:
            res["suggestions"].append("Password reuse detected within the dataset.")
            res["status"] = "Weak (Reused)"
        seen.add(pwd)
        results.append(res)
    return results

def get_policy_template() -> str:
    """Returns a best-practice policy template."""
    return """
Password Policy Recommendation:
- Minimum Length: 12 characters
- Complexity: Require mix of uppercase, lowercase, numbers, and symbols.
- Rotation: Only rotate upon suspected compromise.
- MFA: Multi-Factor Authentication must be enabled.
- Screening: Check against compromised password lists.
"""
