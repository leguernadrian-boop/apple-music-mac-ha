async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    # C'est ici qu'il faut le 's' à setups
    await hass.config_entries.async_forward_entry_setups(entry, ["media_player"])
    return True
