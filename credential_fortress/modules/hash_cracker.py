# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import time
import hashlib
from passlib.hash import md5_crypt, sha256_crypt, sha512_crypt, nthash
import bcrypt

class HashCracker:
    def __init__(self):
        pass

    def crack_unix_hash(self, hash_str: str, wordlist: list[str]) -> tuple[str | None, float]:
        """Attempts to crack a Unix shadow hash using a wordlist. Returns (cracked_password, time_taken)."""
        start_time = time.time()
        
        for word in wordlist:
            if hash_str.startswith('$1$'):
                if md5_crypt.verify(word, hash_str):
                    return word, time.time() - start_time
            elif hash_str.startswith('$5$'):
                if sha256_crypt.verify(word, hash_str):
                    return word, time.time() - start_time
            elif hash_str.startswith('$6$'):
                if sha512_crypt.verify(word, hash_str):
                    return word, time.time() - start_time
            elif hash_str.startswith('$2a$') or hash_str.startswith('$2b$') or hash_str.startswith('$2y$'):
                try:
                    if bcrypt.checkpw(word.encode('utf-8'), hash_str.encode('utf-8')):
                        return word, time.time() - start_time
                except Exception:
                    continue
                    
        return None, time.time() - start_time

    def crack_ntlm_hash(self, hash_str: str, wordlist: list[str]) -> tuple[str | None, float]:
        """Attempts to crack a Windows NTLM hash using a wordlist. Returns (cracked_password, time_taken)."""
        start_time = time.time()
        hash_str = hash_str.lower()
        
        for word in wordlist:
            # NTLM using passlib
            if nthash.verify(word, hash_str):
                return word, time.time() - start_time
                
        return None, time.time() - start_time
        
    def crack_extracted_dataset(self, extracted_hashes: list[dict], wordlist: list[str]) -> dict:
        """
        Runs a dictionary attack against a list of extracted hashes.
        Returns a dict of results mapping usernames to their cracked plaintexts and times.
        """
        results = {
            "total_hashes": len(extracted_hashes),
            "cracked_count": 0,
            "cracked_details": []
        }
        
        for entry in extracted_hashes:
            cracked_pw = None
            time_taken = 0.0
            
            if entry['type'] == 'unix':
                cracked_pw, time_taken = self.crack_unix_hash(entry['hash'], wordlist)
            elif entry['type'] == 'windows':
                cracked_pw, time_taken = self.crack_ntlm_hash(entry['hash'], wordlist)
                
            if cracked_pw:
                results["cracked_count"] += 1
                results["cracked_details"].append({
                    "username": entry['username'],
                    "password": cracked_pw,
                    "algo": entry['algo'],
                    "time_seconds": time_taken
                })
                
        return results
