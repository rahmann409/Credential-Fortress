# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import json
import os
from pathlib import Path
from credential_fortress.modules.logging_audit import audit_log, secure_wipe

def test_audit_log_no_plaintext(tmp_path, monkeypatch):
    test_log = tmp_path / "audit.jsonl"
    monkeypatch.setattr("credential_fortress.modules.logging_audit.LOG_FILE", test_log)
    
    audit_log("test_mod", "test_act", {"param": "value"})
    
    with open(test_log, "r") as f:
        data = json.loads(f.read().strip())
        assert data["module"] == "test_mod"
        assert data["action"] == "test_act"
        assert "encrypted_plaintext" not in data

def test_secure_wipe(tmp_path):
    test_file = tmp_path / "secret.txt"
    with open(test_file, "w") as f:
        f.write("super_secret_data")
        
    assert test_file.exists()
    
    secure_wipe(test_file)
    
    assert not test_file.exists()
