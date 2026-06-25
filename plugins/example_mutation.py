# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

from credential_fortress.modules.plugins import register_mutation

@register_mutation("append_exclamation")
def append_exclamation(word: str) -> list[str]:
    """A simple plugin that appends '!' and '!!' to words."""
    return [word, f"{word}!", f"{word}!!"]
