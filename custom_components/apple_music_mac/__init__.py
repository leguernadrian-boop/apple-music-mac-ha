async def async_setup(hass, config):
    """Configuration via YAML (non utilisée mais requise)."""
    return True

async def async_setup_entry(hass, entry):
    """Configuration via l'interface intuitive (Config Flow)."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "media_player")
    )
    return True