# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

from pathlib import Path
from credential_fortress.modules.safeguards import is_safe_path

class HashExtractor:
    def __init__(self):
        pass

    def extract_unix_shadow(self, file_path: str | Path) -> list[dict]:
        """
        Parses an offline Unix /etc/shadow file dump.
        Expected format: username:hash:lastchanged:min:max:warn:inactive:expire:
        Returns a list of dicts: [{'username': 'user1', 'hash': '$6$salt$hash', 'algo': 'SHA-512'}, ...]
        """
        is_safe_path(file_path)
        extracted = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 2:
                    username = parts[0]
                    hash_str = parts[1]
                    
                    # Ignore locked accounts or empty passwords
                    if hash_str in ('*', '!', '!!', '') or hash_str.startswith('!'):
                        continue
                        
                    algo = "Unknown"
                    if hash_str.startswith('$1$'):
                        algo = "MD5"
                    elif hash_str.startswith('$2a$') or hash_str.startswith('$2b$') or hash_str.startswith('$2y$'):
                        algo = "bcrypt"
                    elif hash_str.startswith('$5$'):
                        algo = "SHA-256"
                    elif hash_str.startswith('$6$'):
                        algo = "SHA-512"
                        
                    extracted.append({
                        'username': username,
                        'hash': hash_str,
                        'algo': algo,
                        'type': 'unix'
                    })
        return extracted

    def extract_windows_pwdump(self, file_path: str | Path) -> list[dict]:
        """
        Parses an offline Windows pwdump format file (extracted from SAM).
        Expected format: Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
        Returns a list of dicts: [{'username': 'Admin', 'hash': 'NTLM_HASH_HERE', 'algo': 'NTLM'}, ...]
        """
        is_safe_path(file_path)
        extracted = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 4:
                    username = parts[0]
                    # NTLM is the 4th part (index 3)
                    ntlm_hash = parts[3].lower()
                    
                    # Ignore empty/disabled hashes
                    if not ntlm_hash or ntlm_hash == "31d6cfe0d16ae931b73c59d7e0c089c0":
                        continue
                        
                    extracted.append({
                        'username': username,
                        'hash': ntlm_hash,
                        'algo': 'NTLM',
                        'type': 'windows'
                    })
        return extracted
