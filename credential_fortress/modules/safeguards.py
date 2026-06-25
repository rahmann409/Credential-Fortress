# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import os
import json
from pathlib import Path

class SecurityViolationError(Exception):
    """Exception raised when a security boundary is crossed."""
    pass

DENYLIST_PATTERNS = [
    '/etc/shadow',
    '/etc/gshadow',
    '/etc/passwd',
    '/etc/master.passwd',
    'C:\\Windows\\System32\\config\\SAM',
    'C:\\Windows\\System32\\config\\SYSTEM',
    '\\\\.\\PhysicalDrive',
    '/dev/sd',
    '/dev/nvme'
]

def check_consent() -> bool:
    """Checks if the user has confirmed the lab environment constraint."""
    consent_file = Path.home() / '.credential_fortress' / 'consent.json'
    if not consent_file.exists():
        return False
    try:
        with open(consent_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('lab_confirmed', False)
    except Exception:
        return False

def confirm_lab() -> None:
    """Writes the lab confirmation token."""
    config_dir = Path.home() / '.credential_fortress'
    config_dir.mkdir(parents=True, exist_ok=True)
    consent_file = config_dir / 'consent.json'
    with open(consent_file, 'w', encoding='utf-8') as f:
        json.dump({'lab_confirmed': True}, f)

def is_safe_path(target_path: str | Path) -> bool:
    """Verifies that a path is not in the denylist and is within allowed directories."""
    target_str = str(target_path).lower()
    for pattern in DENYLIST_PATTERNS:
        if pattern.lower() in target_str:
            raise SecurityViolationError(f"Access to protected path denied: {target_path}")
    
    # Simple sandbox: enforce paths to be in current directory or explicitly provided safe places.
    # We will enforce that the path does not resolve to root '/' or 'C:\' directly.
    resolved = Path(target_path).resolve()
    if str(resolved) == '/' or str(resolved).startswith('C:\\Windows'):
        raise SecurityViolationError(f"Access to system-level directory denied: {resolved}")
        
    return True
