# © 2026 Nasiur Rahman . All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import os
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from credential_fortress.modules.safeguards import check_consent

LOG_FILE = Path("logs/audit.jsonl")

def init_logger() -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def audit_log(module: str, action: str, parameters: dict, include_plaintexts: bool = False, plaintext_data: str = None, encryption_key: bytes = None) -> None:
    """Logs an action. Never logs plaintexts unless explicitly requested and encrypted."""
    init_logger()
    
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "module": module,
        "action": action,
        "parameters": parameters,
        "lab_confirmed": check_consent()
    }
    
    if include_plaintexts and plaintext_data and encryption_key:
        aesgcm = AESGCM(encryption_key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, plaintext_data.encode('utf-8'), None)
        entry["encrypted_plaintext"] = {
            "nonce": nonce.hex(),
            "ciphertext": ct.hex()
        }
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def secure_wipe(target_path: Path) -> None:
    """Performs a basic 3-pass overwrite before unlinking for lab purposes."""
    if not target_path.exists() or not target_path.is_file():
        return
        
    length = target_path.stat().st_size
    try:
        with open(target_path, "ba+", buffering=0) as f:
            for pass_num in range(3):
                f.seek(0)
                # Pass 1: 0x00, Pass 2: 0xFF, Pass 3: Random
                if pass_num == 0:
                    f.write(b'\x00' * length)
                elif pass_num == 1:
                    f.write(b'\xff' * length)
                else:
                    f.write(os.urandom(length))
                os.fsync(f.fileno())
    except Exception as e:
        # If we can't overwrite (e.g. permissions), we still try to remove it.
        pass
        
    os.remove(target_path)
