# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import json
from pathlib import Path
import bcrypt
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from credential_fortress.modules.logging_audit import audit_log

console = Console()

AUTH_FILE = Path.home() / ".credential_fortress" / "auth.json"
WIPED_FILE = Path.home() / ".credential_fortress" / ".wiped"

# Fixed Admin PIN as per requirements
DEFAULT_ADMIN_PIN = "Raj@8340"
DEFAULT_USER_PIN = "74123"

def require_auth() -> None:
    """Prompts for a PIN to unlock the toolkit and determines the user role."""
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if not AUTH_FILE.exists():
        if WIPED_FILE.exists():
            console.print(Panel("[bold magenta]SYSTEM RESTORED: SECURE BOOT[/bold magenta]", border_style="bold blue"))
            while True:
                admin_pwd = Prompt.ask("Set new Admin PIN (8 characters)", password=True)
                admin_confirm = Prompt.ask("Confirm Admin PIN", password=True)
                if admin_pwd == admin_confirm and len(admin_pwd) == 8:
                    admin_hashed = bcrypt.hashpw(admin_pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    break
                else:
                    console.print("[bold red][!] PIN mismatch or not exactly 8 characters. Retry.[/bold red]\n")
            
            while True:
                pwd = Prompt.ask("Set new Normal User PIN (5 digits)", password=True)
                pwd_confirm = Prompt.ask("Confirm Normal User PIN", password=True)
                if pwd == pwd_confirm and len(pwd) == 5 and pwd.isdigit():
                    shared_hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    break
                else:
                    console.print("[bold red][!] PIN mismatch or not exactly 5 digits. Retry.[/bold red]\n")
                    
            with open(AUTH_FILE, "w", encoding="utf-8") as f:
                json.dump({"admin_hash": admin_hashed, "shared_hash": shared_hashed}, f)
            try:
                WIPED_FILE.unlink()
            except Exception:
                pass
            console.print("[bold yellow][+] PINs set successfully. Encryption active.[/bold yellow]\n")
        else:
            # First run, initialize with defaults
            admin_hashed = bcrypt.hashpw(DEFAULT_ADMIN_PIN.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            shared_hashed = bcrypt.hashpw(DEFAULT_USER_PIN.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            with open(AUTH_FILE, "w", encoding="utf-8") as f:
                json.dump({"admin_hash": admin_hashed, "shared_hash": shared_hashed}, f)
    
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        shared_hash = data.get("shared_hash", "")
        
    console.print(Panel("[bold cyan]CREDENTIAL FORTRESS | SECURE TERMINAL[/bold cyan]", border_style="bold magenta"))
    pwd = Prompt.ask("Enter Normal User PIN", password=True)
    
    try:
        if bcrypt.checkpw(pwd.encode('utf-8'), shared_hash.encode('utf-8')):
            audit_log("auth", "login", {"role": "user", "status": "success"})
            console.print("[bold bright_green][+] USER ACCESS GRANTED. WELCOME.[/bold bright_green]\n")
        else:
            audit_log("auth", "login", {"role": "unknown", "status": "denied"})
            console.print("\n[bold red][!] ACCESS DENIED. INTRUSION ATTEMPT LOGGED.[/bold red]")
            exit(1)
    except Exception:
        audit_log("auth", "login", {"role": "unknown", "status": "error"})
        console.print("\n[bold red][!] ACCESS DENIED. CORRUPT SECTOR.[/bold red]")
        exit(1)

def verify_reset_auth() -> bool:
    """Verifies the Admin PIN before allowing a reset or sensitive operation."""
    if not AUTH_FILE.exists():
        return True
        
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        admin_hash = data.get("admin_hash", "")
        
    pwd = Prompt.ask("Enter Admin PIN to authorize (leave blank to skip)", password=True)
    if not pwd:
        audit_log("auth", "admin_verify", {"status": "skipped"})
        return False
        
    try:
        if bcrypt.checkpw(pwd.encode('utf-8'), admin_hash.encode('utf-8')):
            audit_log("auth", "admin_verify", {"status": "success"})
            return True
    except Exception:
        pass
    audit_log("auth", "admin_verify", {"status": "denied"})
    return False

def change_pins() -> None:
    if not verify_reset_auth():
        console.print("[bold red]Authorization failed. Cannot change PINs.[/bold red]")
        return
        
    choice = Prompt.ask("Change (1) Admin PIN or (2) Normal User PIN? [1/2]", choices=["1", "2"], show_choices=False)
    
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if choice == "1":
        new_pin = Prompt.ask("Enter new Admin PIN (exactly 8 characters)", password=True)
        confirm_pin = Prompt.ask("Confirm new Admin PIN", password=True)
        if new_pin == confirm_pin and len(new_pin) == 8:
            data["admin_hash"] = bcrypt.hashpw(new_pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            with open(AUTH_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f)
            audit_log("auth", "change_pin", {"target": "admin", "status": "success"})
            console.print("[green]Admin PIN updated successfully.[/green]")
        else:
            console.print("[bold red]Mismatch or invalid length. Must be exactly 8 characters.[/bold red]")
            audit_log("auth", "change_pin", {"target": "admin", "status": "failed"})
    elif choice == "2":
        new_pin = Prompt.ask("Enter new Normal User PIN (exactly 5 digits)", password=True)
        confirm_pin = Prompt.ask("Confirm new Normal User PIN", password=True)
        if new_pin == confirm_pin and len(new_pin) == 5 and new_pin.isdigit():
            data["shared_hash"] = bcrypt.hashpw(new_pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            with open(AUTH_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f)
            audit_log("auth", "change_pin", {"target": "shared", "status": "success"})
            console.print("[green]Normal User PIN updated successfully.[/green]")
        else:
            console.print("[bold red]Mismatch or invalid format. Must be exactly 5 digits.[/bold red]")
            audit_log("auth", "change_pin", {"target": "shared", "status": "failed"})
