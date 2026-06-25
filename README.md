# Credential Fortress 🏰

*Crafted by Raj - राजेन निर्मितम्*

Welcome to **Credential Fortress**! Think of this as a safe, simulated training ground to learn about password security. 

Whether you're a cybersecurity student, an instructor, or just someone curious about how passwords get compromised, this tool lets you safely explore the mechanics of password strength without ever touching real, sensitive data.

---

## What Does It Do? (In Simple Terms)

Imagine you have a lock (a password hash) and a huge ring of keys (a dictionary of guesses). Hackers use powerful computers to try millions of keys per second. 

**Credential Fortress** helps you understand this process by:
1. **Generating "Keys":** It can take a few simple words (like your name or pet's name) and mutate them just like a hacker would—adding numbers, changing "e" to "3", or adding exclamation marks.
2. **Making Fake "Locks":** It takes your test words and creates safe, fake password hashes (like the ones stored in a database). 
3. **Simulating the Break-in:** It calculates exactly how long it would take a hacker's computer to crack those passwords. (For example: A simple password might take "Instant (< 1 second)", while a strong one might take "> 1000 years").
4. **Grading Your Passwords:** It analyzes your passwords and gives you a report card on how strong they are and how to make them better.

**The best part?** It's all a simulation! It never looks at your real computer passwords, making it 100% safe to use in a lab or classroom.

---

## Professional Overview

**Credential Fortress** is an educational, simulation-only password assessment toolkit designed for controlled lab environments, training sessions, and defensive research. 

It provides an interactive terminal interface (CLI) to demonstrate dictionary generation, hash simulation, and time-to-crack estimations. 

### Key Features
* **Safe Sandbox:** Actively denies access to operating system credential stores (like `/etc/shadow` or Windows SAM). It operates strictly on synthetic, user-provided datasets.
* **Audit Logging:** Every simulation is logged for accountability. By default, plaintext secrets are stripped from the logs to prevent accidental exposure.
* **Dictionary Mutation Engine:** Generates realistic password guessing lists using built-in leet-speak and pattern rules.
* **Brute-Force & Hash Simulators:** Emulates MD5, SHA-256, and bcrypt hashing and provides accurate mathematical models for crack-time estimations.
* **Plugin Architecture:** Highly extensible. Developers can easily write Python plugins to introduce new mutation algorithms or hash types.
* **Automated Reporting:** Generates professional PDF audit reports summarizing the simulated vulnerability of a given dataset.

---

## 🚀 How to Use It

### 1. Installation & Setup
First, make sure you have **Python 3.10 or newer** installed. It is highly recommended to use a virtual environment so you don't clutter your system's Python with project dependencies.

**For Linux / macOS:**
Open your terminal and run the following commands one by one:
```bash
# 1. Create a virtual environment named "venv"
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Install the tool and all its dependencies
pip install -e .[dev]
```

**For Windows:**
Open PowerShell or Command Prompt and run the following commands one by one:
```powershell
# 1. Create a virtual environment named "venv"
python -m venv venv

# 2. Activate the virtual environment
.\venv\Scripts\activate

# 3. Install the tool and all its dependencies
pip install -e .[dev]
```

### 2. Getting Started
*(Make sure your virtual environment is still activated! You will know it is activated if you see `(venv)` at the start of your terminal prompt.)*

To launch the interactive tool, simply run:
```bash
python -m credential_fortress.main
```
*(Note: On your very first run, you will be required to set a **Master Password** to lock the toolkit and confirm that you are running this in a safe lab environment.)*

### 3. Generate Some Practice Data
Don't have any test passwords? No problem! You can ask the tool to generate some safe, fake scenarios for you:
```bash
python -m credential_fortress.main --generate-sample
```
This will create three practice files in the `data/` folder: weak passwords, pattern-based passwords, and strong passwords.

### 4. Run an Analysis
Want to see how fast a weak password falls? Run an analysis in "dry-run" mode (which means it won't write a bunch of heavy files to your hard drive):
```bash
python -m credential_fortress.main --scenario data/scenario1_weak.txt --dry-run
```

### 5. Secure Cleanup
If you want to quickly reset your lab environment, the Main Menu includes a **Clean Generated Data (Secure Wipe)** option. You can also run this directly from your terminal using:
```bash
python -m credential_fortress.main --cleanup
```
This executes a 3-pass overwrite to completely destroy all generated dictionaries, password hashes, simulation reports, and logs. It also gives you the option to permanently wipe your Master Password!

---

## Ethical Constraints & Safety Notice
This tool was crafted with safety as the top priority. 
- **No real credential harvesting:** The tool will throw a `SecurityViolationError` if you try to feed it real system files.
- **No network calls:** The simulation runs entirely locally on your machine.
- **Telemetry-free:** Local metrics are saved to `reports/metrics.csv` for your eyes only.

Please use this software responsibly, legally, and purely for educational defense.

---

## Legal Notice
© 2026 Raj Kumar. All rights reserved.
- **Copyrighted Material:** This toolkit is strictly protected under copyright law.
- **Educational Use Only:** It is intended exclusively for controlled lab environments and simulations.
- **Restrictions:** Unauthorized commercial use, redistribution, or modification of this toolkit without explicit written permission from the author is strictly prohibited. See the `LICENSE` file for full terms.
