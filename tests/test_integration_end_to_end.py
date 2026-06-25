# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import subprocess
import sys
from pathlib import Path

def test_dry_run_does_not_create_files(tmp_path, monkeypatch):
    # Call the module via subprocess with --dry-run
    # First we need to generate samples so the scenario exists
    subprocess.run([sys.executable, "-m", "credential_fortress.main", "--generate-sample", "--dry-run"], check=True)
    
    # Actually create the sample for the next step just to be safe
    subprocess.run([sys.executable, "-m", "credential_fortress.main", "--generate-sample"], check=True)
    
    # Run the dry run
    result = subprocess.run([sys.executable, "-m", "credential_fortress.main", "--scenario", "data/scenario1_weak.txt", "--dry-run"], capture_output=True, text=True)
    
    assert result.returncode == 0
    assert "Analyzing" in result.stdout
    assert "Brute force simulation" in result.stdout
    
    # Verify no output files were generated during the dry run
    # (Output dir should be empty or not contain the specific dict_scenario1_weak.txt)
    output_dict = Path("output/dict_scenario1_weak.txt")
    assert not output_dict.exists()
