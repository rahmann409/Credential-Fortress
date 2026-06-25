# Plugin Development Guide

Credential Fortress supports a simple plugin API for:
- Custom mutation rules.
- Additional simulated hash algorithms.
- Custom report formats.

## Creating a Plugin
1. Create a Python file in `plugins/` (e.g., `my_plugin.py`).
2. Implement the required functions.
3. Use the `@register_mutation` or `@register_algorithm` decorators from `credential_fortress.modules.plugins`.

See `plugins/example_mutation.py` for a complete example.
