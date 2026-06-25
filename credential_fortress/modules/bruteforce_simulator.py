# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import math
from typing import Dict, Any

def calculate_search_space(length: int, use_lower: bool, use_upper: bool, use_digits: bool, use_symbols: bool) -> int:
    """Calculates the total possible combinations for a given length and character set."""
    charset_size = 0
    if use_lower: charset_size += 26
    if use_upper: charset_size += 26
    if use_digits: charset_size += 10
    if use_symbols: charset_size += 32
    
    if charset_size == 0:
        return 0
        
    return charset_size ** length

def estimate_crack_time(combinations: int, hash_rate: int) -> float:
    """Estimates time to crack in seconds."""
    if hash_rate <= 0:
        return float('inf')
    return combinations / hash_rate

def format_time(seconds: float) -> str:
    """Formats seconds into human-readable time."""
    if seconds == float('inf'):
        return "Infinity"
    if seconds < 1:
        return "Instant (< 1 second)"
    
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    years = days / 365
    
    if years > 1000:
        return f"> 1000 years"
    if years > 1:
        return f"{years:.1f} years"
    if days > 1:
        return f"{days:.1f} days"
    if hours > 1:
        return f"{hours:.1f} hours"
    if minutes > 1:
        return f"{minutes:.1f} minutes"
        
    return f"{seconds:.1f} seconds"

def simulate_bruteforce(target_password: str, hash_rate: int) -> Dict[str, Any]:
    """Simulates a brute-force attack to estimate time required to guess the password."""
    length = len(target_password)
    has_lower = any(c.islower() for c in target_password)
    has_upper = any(c.isupper() for c in target_password)
    has_digits = any(c.isdigit() for c in target_password)
    has_symbols = not target_password.isalnum()
    
    combinations = calculate_search_space(length, has_lower, has_upper, has_digits, has_symbols)
    time_seconds = estimate_crack_time(combinations, hash_rate)
    
    return {
        "password_length": length,
        "combinations": combinations,
        "estimated_time_seconds": time_seconds,
        "formatted_time": format_time(time_seconds),
        "charset_used": {
            "lower": has_lower,
            "upper": has_upper,
            "digits": has_digits,
            "symbols": has_symbols
        }
    }
