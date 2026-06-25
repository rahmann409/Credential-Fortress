# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import pytest
from pathlib import Path
from credential_fortress.modules.safeguards import is_safe_path, SecurityViolationError

def test_is_safe_path_allowed():
    # Relative or data paths should be allowed
    assert is_safe_path("data/scenario1.txt") is True
    assert is_safe_path(Path("data/output.txt")) is True

def test_is_safe_path_denied():
    with pytest.raises(SecurityViolationError):
        is_safe_path("/etc/shadow")
        
    with pytest.raises(SecurityViolationError):
        is_safe_path("C:\\Windows\\System32\\config\\SAM")
        
    with pytest.raises(SecurityViolationError):
        is_safe_path("/dev/sdX")

def test_is_safe_path_case_insensitive():
    with pytest.raises(SecurityViolationError):
        is_safe_path("/ETC/SHADOW")
