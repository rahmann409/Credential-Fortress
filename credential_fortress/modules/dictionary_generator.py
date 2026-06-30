# © 2026 Nasiur Rahman. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

from pathlib import Path
from typing import List, Set
from credential_fortress.modules.safeguards import is_safe_path

LEET_MAP = {
    'a': ['4', '@'],
    'e': ['3'],
    'i': ['1', '!'],
    'o': ['0'],
    's': ['$', '5'],
    't': ['7']
}

def apply_leet_speak(word: str) -> List[str]:
    """Generates leet speak variations of a word recursively."""
    results = {word}
    for char, replacements in LEET_MAP.items():
        new_results = set()
        for w in results:
            if char in w.lower():
                for rep in replacements:
                    new_results.add(w.replace(char, rep))
                    new_results.add(w.replace(char.upper(), rep))
        results.update(new_results)
    return list(results)

def apply_case_variations(word: str) -> List[str]:
    """Returns variations of casing."""
    return list({word.lower(), word.upper(), word.capitalize()})

def append_common_numbers(word: str) -> List[str]:
    """Appends common numbers like years or sequences."""
    suffixes = ['123', '1', '12', '2023', '2024', '99']
    return [f"{word}{s}" for s in suffixes]

def generate_dictionary(base_words: List[str], use_leet: bool = True, use_case: bool = True, use_numbers: bool = True) -> List[str]:
    """Generates a mutated dictionary from base words."""
    result: Set[str] = set(base_words)
    
    current_words = list(result)
    
    if use_case:
        for w in current_words:
            result.update(apply_case_variations(w))
            
    current_words = list(result)
    if use_leet:
        for w in current_words:
            result.update(apply_leet_speak(w))
            
    current_words = list(result)
    if use_numbers:
        for w in current_words:
            result.update(append_common_numbers(w))
            
    return sorted(list(result))

def save_dictionary(words: List[str], target_path: str | Path) -> None:
    """Saves the generated dictionary to a file safely."""
    is_safe_path(target_path)
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, 'w', encoding='utf-8') as f:
        for word in words:
            f.write(f"{word}\n")
