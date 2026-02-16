async def async_setup(hass, config):
    """Configuration via YAML (non utilisée)."""
    return True

async def async_setup_entry(hass, entry):
    """Configuration via l'interface."""
    # On ajoute un 's' à setups et on met le domaine dans une liste []
    await hass.config_entries.async_forward_entry_setups(entry, ["media_player"])
    return True
