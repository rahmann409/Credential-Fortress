# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

from typing import Callable, Dict, List

MUTATION_PLUGINS: Dict[str, Callable[[str], List[str]]] = {}
ALGORITHM_PLUGINS: Dict[str, Callable[[str], str]] = {}

def register_mutation(name: str):
    def decorator(func: Callable[[str], List[str]]):
        MUTATION_PLUGINS[name] = func
        return func
    return decorator

def register_algorithm(name: str):
    def decorator(func: Callable[[str], str]):
        ALGORITHM_PLUGINS[name] = func
        return func
    return decorator

def load_plugins() -> None:
    """Dynamically loads plugins from the plugins directory."""
    import importlib
    import pkgutil
    import sys
    from pathlib import Path
    
    plugins_dir = Path("plugins")
    if not plugins_dir.exists():
        return
        
    sys.path.insert(0, str(plugins_dir.parent))
    
    for _, module_name, _ in pkgutil.iter_modules([str(plugins_dir)]):
        try:
            importlib.import_module(f"plugins.{module_name}")
        except Exception as e:
            # Safely ignore plugin load errors in production, but could log them
            pass
            
    sys.path.pop(0)
