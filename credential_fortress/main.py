# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import os
import sys
import argparse
import random
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from credential_fortress.modules.safeguards import check_consent, confirm_lab, is_safe_path
from credential_fortress.modules.auth import require_auth
from credential_fortress.modules.logging_audit import audit_log, secure_wipe
from credential_fortress.modules.metrics import record_metric
from credential_fortress.modules.dictionary_generator import generate_dictionary, save_dictionary
from credential_fortress.modules.hash_simulator import simulate_hashes, save_simulated_hashes
from credential_fortress.modules.bruteforce_simulator import simulate_bruteforce
from credential_fortress.modules.analyzer import analyze_dataset, get_policy_template
from credential_fortress.modules.report_generator import generate_pdf_report, generate_txt_report
from credential_fortress.modules.plugins import load_plugins
from credential_fortress.modules.hash_extractor import HashExtractor
from credential_fortress.modules.hash_cracker import HashCracker

console = Console()

QUOTES = [
    ("विद्या धनं सर्वधनप्रधानम्", "Knowledge is the supreme wealth."),
    ("सत्यं शिवं सुंदरम्", "Truth is auspicious and beautiful.")
]

def show_banner():
    banner_path = Path("data/banners/banner1.txt")
    if banner_path.exists():
        with open(banner_path, "r", encoding="utf-8") as f:
            ascii_art = f.read()
            panel = Panel(f"[bold cyan]{ascii_art}[/bold cyan]", border_style="bold magenta", title="[bold yellow]SYS.INIT[/bold yellow]", subtitle="[bold blue]v1.0.0[/bold blue]")
            console.print(panel)
    else:
        console.print(Panel("[bold cyan]Credential Fortress - Crafted by Raj[/bold cyan]", border_style="bold magenta", title="[bold yellow]SYS.INIT[/bold yellow]"))
        
    quote, trans = random.choice(QUOTES)
    console.print(f"  [bold bright_black]>[/bold bright_black] [bold magenta]{quote}[/bold magenta] [dim white]- {trans}[/dim white]\n")

def check_lab_consent():
    if not check_consent():
        console.print(Panel("[red]ETHICAL USE NOTICE[/red]\nThis tool is strictly for educational, simulation-only password assessment. Do not run on production systems or try to access real OS credential stores.", border_style="red"))
        if Confirm.ask("Do you confirm you are in a controlled lab environment?"):
            confirm_lab()
            audit_log("system", "consent_granted", {})
        else:
            console.print("[red]Consent required to proceed. Exiting.[/red]")
            sys.exit(1)

def run_generate_sample(dry_run: bool):
    """Generates the three synthetic scenarios."""
    console.print("[green]Generating synthetic sample data...[/green]")
    scenarios = {
        "scenario1_weak.txt": ["password", "123456", "qwerty"],
        "scenario2_patterns.txt": ["John1980", "Alice2023"],
        "scenario3_strong.txt": ["H$8x9!kLp2@z"]
    }
    
    Path("data").mkdir(exist_ok=True)
    
    for filename, words in scenarios.items():
        filepath = Path("data") / filename
        if not dry_run:
            save_dictionary(words, filepath)
            console.print(f"Created {filepath}")
            
    audit_log("fortress", "generate_samples", {"dry_run": dry_run})

def run_cleanup():
    from credential_fortress.modules.auth import verify_reset_auth
    
    console.print("\n[bold red]WARNING: This will securely wipe all generated scenarios, hashes, dictionaries, logs, and reports.[/bold red]")
    if Confirm.ask("Are you sure you want to securely wipe all data?"):
        console.print("\n[bold yellow]Admin Authorization Required for Data Wipe[/bold yellow]")
        if not verify_reset_auth():
            console.print("[bold red]Admin PIN verification failed. Aborting secure wipe.[/bold red]")
            return
            
        # Wipe scenario files safely without deleting banners
        for p in Path("data").glob("scenario*.txt"):
            if p.is_file():
                secure_wipe(p)
                
        # Wipe generated folders
        folders_to_clean = ["output", "samples", "reports", "logs"]
        for d in folders_to_clean:
            path = Path(d)
            if path.exists() and path.is_dir():
                for p in path.rglob('*'):
                    if p.is_file():
                        secure_wipe(p)
                try:
                    shutil.rmtree(path)
                except Exception:
                    pass
                    
        # Wipe auth file and set .wiped flag
        from credential_fortress.modules.auth import AUTH_FILE, WIPED_FILE, secure_wipe
        if AUTH_FILE.exists():
            secure_wipe(AUTH_FILE)
            try:
                AUTH_FILE.unlink()
            except Exception:
                pass
        try:
            WIPED_FILE.touch()
        except Exception:
            pass
            
        console.print("[green]Data wipe complete! The tool will now exit to regenerate passwords on next run.[/green]")
        sys.exit(0)

def run_analysis(scenario_path: str, dry_run: bool):
    try:
        is_safe_path(scenario_path)
        with open(scenario_path, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
            
        console.print(f"\n[bold]Analyzing {len(words)} passwords from {scenario_path}[/bold]")
        
        # Simulate dictionary generation
        dict_words = generate_dictionary(words)
        if not dry_run:
            save_dictionary(dict_words, f"output/dict_{Path(scenario_path).name}")
            
        # Simulate Hashes
        hashes = simulate_hashes(words)
        if not dry_run:
            Path("output").mkdir(exist_ok=True)
            save_simulated_hashes(hashes, f"output/hashes_{Path(scenario_path).name}")
            
        # Simulate bruteforce for the first word
        if words:
            bf_stats = simulate_bruteforce(words[0], 1000000)
            console.print(f"\n[bold]Attack Simulation for first entry:[/bold]")
            console.print(f"1. [yellow]Exhaustive Brute Force[/yellow] (Trying every combination of a-z) @ 1M H/s: {bf_stats['formatted_time']}")
            
            # Dictionary attack check
            is_in_dict = words[0].lower() in [w.lower() for w in dict_words]
            if is_in_dict:
                console.print(f"2. [red]Dictionary Attack[/red] (Using wordlists & mutations) @ 1M H/s: [red]Instant (< 1 second)[/red] (Match found!)")
            else:
                console.print(f"2. [green]Dictionary Attack[/green] (Using wordlists & mutations) @ 1M H/s: [green]Failed[/green] (Not in dictionary)")
            
        # Analyze Dataset
        results = analyze_dataset(words, dict_words)
        
        if not dry_run:
            Path("samples/reports").mkdir(parents=True, exist_ok=True)
            pdf_path = f"samples/reports/report_{Path(scenario_path).stem}.pdf"
            generate_pdf_report(results, pdf_path)
            console.print(f"[green]Report generated at {pdf_path}[/green]")
            
        audit_log("fortress", "analysis_run", {"scenario": scenario_path, "dry_run": dry_run})
        record_metric(scenario_path, len(dict_words), 1000000, bf_stats['estimated_time_seconds'] if words else 0.0, 1.5)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

def main() -> None:
    # 1. Lock the toolkit immediately
    require_auth()
    
    # 2. Setup CLI arguments
    parser = argparse.ArgumentParser(description="Credential Fortress (Educational)")
    parser.add_argument("--scenario", type=str, help="Path to scenario file to run analysis on")
    parser.add_argument("--dry-run", action="store_true", help="Run without writing files")
    parser.add_argument("--generate-sample", action="store_true", help="Generate synthetic samples")
    parser.add_argument("--ansi-fallback", action="store_true", help="Use basic ANSI output")
    parser.add_argument("--cleanup", action="store_true", help="Securely wipe all generated data")
    parser.add_argument("--reveal-admin-pin", action="store_true", help="Attempt to reveal the Admin PIN")
    
    # Hash Extraction & Cracking Args
    parser.add_argument("--shadow", type=str, help="Path to offline Linux /etc/shadow file dump")
    parser.add_argument("--pwdump", type=str, help="Path to offline Windows pwdump format file")
    parser.add_argument("--crack-with", type=str, help="Wordlist to use for dictionary attack against extracted hashes")
    
    args = parser.parse_args()
    
    if args.reveal_admin_pin:
        console.print("[bold red]Access denied. The Admin PIN cannot be revealed.[/bold red]")
        sys.exit(1)
        
    load_plugins()
    check_lab_consent()
    
    if not args.ansi_fallback:
        show_banner()
        
    if args.cleanup:
        run_cleanup()
        return
        
    if args.generate_sample:
        run_generate_sample(args.dry_run)
        if not args.scenario:
            return

    if args.scenario:
        run_analysis(args.scenario, args.dry_run)
            
    elif args.shadow or args.pwdump:
        if not args.crack_with:
            console.print("[red]Error: You must provide a wordlist using --crack-with to attack the hashes.[/red]")
            sys.exit(1)
            
        try:
            extractor = HashExtractor()
            cracker = HashCracker()
            extracted = []
            
            if args.shadow:
                console.print(f"[bold]Extracting hashes from offline shadow file: {args.shadow}[/bold]")
                extracted.extend(extractor.extract_unix_shadow(args.shadow))
            
            if args.pwdump:
                console.print(f"[bold]Extracting hashes from offline pwdump file: {args.pwdump}[/bold]")
                extracted.extend(extractor.extract_windows_pwdump(args.pwdump))
                
            console.print(f"[green]Successfully extracted {len(extracted)} valid hashes.[/green]")
            
            with open(args.crack_with, 'r', encoding='utf-8') as f:
                wordlist = [line.strip() for line in f if line.strip()]
                
            console.print(f"Starting dictionary attack using {len(wordlist)} words...")
            
            results = cracker.crack_extracted_dataset(extracted, wordlist)
            
            console.print(f"\n[bold]Cracking Results:[/bold]")
            console.print(f"Total Hashes: {results['total_hashes']}")
            console.print(f"Successfully Cracked: [green]{results['cracked_count']}[/green]")
            
            if results["cracked_count"] > 0:
                table = Table(title="Compromised Accounts")
                table.add_column("Username", style="cyan")
                table.add_column("Password", style="red")
                table.add_column("Algorithm", style="magenta")
                table.add_column("Time Taken", justify="right")
                
                for res in results["cracked_details"]:
                    table.add_row(res["username"], res["password"], res["algo"], f"{res['time_seconds']:.4f}s")
                
                console.print(table)
            
            audit_log("fortress", "crack_simulation", {"cracked_count": results["cracked_count"]})
            
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)
    else:
        # Interactive Menu
        while True:
            menu_text = (
                "[bold yellow]1.[/bold yellow] [bright_cyan]Generate Synthetic Samples[/bright_cyan]\n"
                "[bold yellow]2.[/bold yellow] [bright_cyan]Run Scenario (Weak)[/bright_cyan]\n"
                "[bold yellow]3.[/bold yellow] [bright_cyan]Policy Recommendations[/bright_cyan]\n"
                "[bold yellow]4.[/bold yellow] [bright_cyan]Extract & Crack Offline Hashes (Demo)[/bright_cyan]\n"
                "[bold yellow]5.[/bold yellow] [bright_cyan]Clean Generated Data (Secure Wipe)[/bright_cyan]\n"
                "[bold yellow]6.[/bold yellow] [bright_cyan]Manage Security Settings (Change PINs)[/bright_cyan]\n"
                "[bold yellow]7.[/bold yellow] [bold red]Terminate Connection[/bold red]"
            )
            console.print(Panel(menu_text, title="[bold red]COMMAND.MATRIX[/bold red]", border_style="bold blue", width=65))
            
            choice = Prompt.ask("[bold magenta]root[/bold magenta][bold white]@[/bold white][bold yellow]cred-fortress[/bold yellow][bold white]:[/bold white][bold cyan]~[/bold cyan][bold red]$[/bold red]", choices=["1", "2", "3", "4", "5", "6", "7"], show_choices=False)
            
            if choice == "1":
                run_generate_sample(False)
            elif choice == "2":
                run_analysis("data/scenario1_weak.txt", True)
            elif choice == "3":
                console.print(Panel(get_policy_template(), title="Best Practices"))
            elif choice == "4":
                console.print("\n[yellow]To run a dictionary attack on offline hashes, use the CLI. Example:[/yellow]")
                console.print("python -m credential_fortress.main --shadow data/dummy_shadow.txt --crack-with data/scenario1_weak.txt\n")
            elif choice == "5":
                run_cleanup()
            elif choice == "6":
                from credential_fortress.modules.auth import change_pins
                change_pins()
            elif choice == "7":
                break

if __name__ == "__main__":
    main()
