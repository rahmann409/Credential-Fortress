# © 2026 Nasiur Rahman. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import hashlib
from typing import List, Dict
from passlib.hash import bcrypt
from credential_fortress.modules.safeguards import is_safe_path
from datetime import datetime, timezone

def generate_md5(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

def generate_sha256(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_bcrypt(password: str) -> str:
    # Use lowest rounds for simulation speed if processing large lists, but 10 is standard.
    return bcrypt.using(rounds=4).hash(password)

ALGORITHMS = {
    'md5': generate_md5,
    'sha256': generate_sha256,
    'bcrypt': generate_bcrypt
}

def simulate_hashes(plaintexts: List[str], algorithm: str = 'sha256') -> List[Dict[str, str]]:
    """Generates synthetic hashes from plaintexts."""
    if algorithm not in ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
        
    func = ALGORITHMS[algorithm]
    results = []
    
    for pwd in plaintexts:
        results.append({
            "plaintext": pwd,  # Only kept in memory or safe simulation outputs
            "hash": func(pwd),
            "algorithm": algorithm,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
        
    return results

def save_simulated_hashes(hash_data: List[Dict[str, str]], target_path: str, include_plaintext: bool = False) -> None:
    """Saves simulated hashes to a file. Optionally omits the plaintext mapping."""
    is_safe_path(target_path)
    import json
    
    output = []
    for hd in hash_data:
        entry = hd.copy()
        if not include_plaintext:
            entry.pop("plaintext", None)
        output.append(entry)
        
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)
