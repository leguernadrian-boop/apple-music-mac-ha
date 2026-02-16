from homeassistant import config_entries
import voluptuous as vol

class AppleMusicFlow(config_entries.ConfigFlow, domain="apple_music_mac"):
    """Gestion de l'installation intuitive."""
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Crée l'appareil avec le nom de ton choix
            return self.async_create_entry(title="Apple Music Mac", data=user_input)
        
        # Formulaire qui demande l'IP et le Port (8181 par défaut)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host", default="192.168.1.65"): str,
                vol.Required("port", default=8181): int,
            })
        )