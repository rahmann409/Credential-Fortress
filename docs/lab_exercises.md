# Lab Exercises

These exercises guide you through the features of Credential Fortress.

## Exercise 1: Weak Common Passwords
1. **Objective:** Understand how quickly simple passwords can be simulated as cracked.
2. **Steps:**
   - Run: `python -m credential_fortress.main --scenario data/scenario1_weak.txt --dry-run`
   - Review the generated metrics and estimated time-to-crack.
   - Note how fast the dictionary overlap detects these.

## Exercise 2: Pattern-Based Passwords
1. **Objective:** Learn how name+date combinations are vulnerable.
2. **Steps:**
   - Run: `python -m credential_fortress.main --scenario data/scenario2_patterns.txt --dry-run`
   - Check the mutation generator outputs to see how `John1980` is generated from base words.

## Exercise 3: High-Entropy Passwords
1. **Objective:** See how strong passwords resist standard dictionary generation.
2. **Steps:**
   - Run: `python -m credential_fortress.main --scenario data/scenario3_strong.txt --dry-run`
   - Note the extended estimated time-to-crack.
