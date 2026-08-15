"""
Centralized Template Registry & Dynamic Exposer.

Purpose:
    Serves as the single authoritative registry for all resume layout templates.
    Exposes TEMPLATE_REGISTRY and helper resolution functions to eliminate duplicate template mappings.
"""

from typing import Dict, Any
import templates.ats_professional as ats_professional
import templates.modern_professional as modern_professional
import templates.developer_professional as developer_professional

# Centralized Template Registry
TEMPLATE_REGISTRY: Dict[str, Any] = {
    ats_professional.KEY: ats_professional,
    modern_professional.KEY: modern_professional,
    developer_professional.KEY: developer_professional,
}


def get_template_registry() -> Dict[str, Any]:
    """Returns dictionary mapping template keys to loaded template modules."""
    return TEMPLATE_REGISTRY


def get_template_module(key: str) -> Any:
    """Resolves template module object from template key string.

    Args:
        key: Template key identifier ('ats_professional', 'modern_professional', 'developer_professional').

    Returns:
        Template module object. Defaults to modern_professional if unmapped.
    """
    clean_key = (key or "").strip().lower()
    for reg_key, mod in TEMPLATE_REGISTRY.items():
        if reg_key in clean_key or clean_key in reg_key:
            return mod
    return modern_professional
