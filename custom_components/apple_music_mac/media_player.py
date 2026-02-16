import requests
import logging
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    SUPPORT_PLAY, SUPPORT_PAUSE, SUPPORT_NEXT_TRACK, 
    SUPPORT_PREVIOUS_TRACK, SUPPORT_VOLUME_SET
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    host = config_entry.data.get("host")
    port = config_entry.data.get("port")
    async_add_entities([AppleMusicModern(host, port)])

class AppleMusicModern(MediaPlayerEntity):
    def __init__(self, host, port):
        self._url = f"http://{host}:{port}"
        self._attr_name = "Apple Music Mac"
        self._attr_unique_id = f"apple_music_mac_{host}" # ID Unique pour éviter l'échec
        self._state = "off"
        self._title = None
        self._artist = None

    @property
    def state(self): return self._state
    @property
    def media_title(self): return self._title
    @property
    def media_artist(self): return self._artist
    @property
    def supported_features(self):
        return SUPPORT_PLAY | SUPPORT_PAUSE | SUPPORT_NEXT_TRACK | SUPPORT_PREVIOUS_TRACK | SUPPORT_VOLUME_SET

    def update(self):
        try:
            r = requests.get(f"{self._url}/now_playing", timeout=2)
            if r.status_code == 200:
                data = r.json()
                self._title = data.get("name")
                self._artist = data.get("artist")
                state = data.get("player_state")
                self._state = "playing" if state == "playing" else "paused"
            else:
                self._state = "off"
        except Exception:
            self._state = "off"

    def media_play(self): requests.put(f"{self._url}/play")
    def media_pause(self): requests.put(f"{self._url}/pause")
    def media_next_track(self): requests.put(f"{self._url}/next")
    def media_previous_track(self): requests.put(f"{self._url}/previous")
