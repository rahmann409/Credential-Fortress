# Threat Model

## Purpose
Credential Fortress is designed exclusively for educational simulations. It teaches defensive security principles regarding password strength and dictionary generation.

## In Scope (What it does)
- Evaluates the strength of user-supplied or synthetic password lists.
- Generates simulated password hashes.
- Simulates brute-force and dictionary attacks computationally.
- Computes time-to-crack estimates using hypothetical hash rates.

## Out of Scope (What it explicitly avoids)
- Cracking real system passwords.
- Exploiting active directories or network services.
- Reading local OS credential stores (e.g., `/etc/shadow`, Windows SAM).

## Misuse Risks & Mitigations
- **Risk:** Accidental execution on real production datasets.
  - **Mitigation:** The application implements a path denylist and sandbox enforcement. It requires an explicit `--confirm-lab` one-time token.
- **Risk:** Exposing plaintexts in logs.
  - **Mitigation:** Structured audit logging explicitly strips plaintext secrets unless the user securely opts in (with AES-GCM encryption).
