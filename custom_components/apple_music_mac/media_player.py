import requests
import logging
import urllib.parse
from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature
from homeassistant.const import STATE_PLAYING, STATE_PAUSED, STATE_OFF

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    host = config_entry.data.get("host")
    port = config_entry.data.get("port")
    async_add_entities([AppleMusicModern(host, port)])

class AppleMusicModern(MediaPlayerEntity):
    def __init__(self, host, port):
        self._url = f"http://{host}:{port}"
        self._attr_name = "Apple Music Mac"
        self._attr_unique_id = f"apple_music_mac_{host}"
        self._state = STATE_OFF
        self._title = None
        self._artist = None
        self._album = None
        self._volume = 0
        self._image_url = None

    @property
    def state(self): return self._state
    @property
    def media_title(self): return self._title
    @property
    def media_artist(self): return self._artist
    @property
    def media_album_name(self): return self._album
    @property
    def volume_level(self): return self._volume
    @property
    def media_image_url(self): return self._image_url # L'URL de la pochette

    @property
    def supported_features(self):
        return (
            MediaPlayerEntityFeature.PLAY
            | MediaPlayerEntityFeature.PAUSE
            | MediaPlayerEntityFeature.NEXT_TRACK
            | MediaPlayerEntityFeature.PREVIOUS_TRACK
            | MediaPlayerEntityFeature.VOLUME_SET
        )

    def update(self):
        try:
            # 1. On demande les infos au Mac
            r = requests.get(f"{self._url}/now_playing", timeout=2)
            if r.status_code == 200:
                data = r.json()
                new_title = data.get("name")
                new_artist = data.get("artist")
                
                # Si la chanson a changé, on cherche la nouvelle pochette
                if new_title != self._title:
                    self._fetch_artwork(new_artist, new_title)

                self._title = new_title
                self._artist = new_artist
                self._album = data.get("album")
                self._volume = data.get("volume", 0) / 100
                
                state = data.get("player_state")
                if state == "playing": self._state = STATE_PLAYING
                elif state == "paused": self._state = STATE_PAUSED
                else: self._state = STATE_OFF
            else:
                self._state = STATE_OFF
        except Exception:
            self._state = STATE_OFF

    def _fetch_artwork(self, artist, title):
        """Cherche la pochette sur iTunes API"""
        if not artist or not title:
            self._image_url = None
            return
        try:
            # On cherche sur l'API publique d'Apple
            query = urllib.parse.quote(f"{artist} {title}")
            api_url = f"https://itunes.apple.com/search?term={query}&limit=1&media=music"
            res = requests.get(api_url, timeout=3).json()
            if res["resultCount"] > 0:
                # On prend l'image et on demande une version 600x600 (meilleure qualité)
                artwork = res["results"][0]["artworkUrl100"]
                self._image_url = artwork.replace("100x100", "600x600")
            else:
                self._image_url = None
        except Exception:
            self._image_url = None

    def media_play(self): requests.put(f"{self._url}/play")
    def media_pause(self): requests.put(f"{self._url}/pause")
    def media_next_track(self): requests.put(f"{self._url}/next")
    def media_previous_track(self): requests.put(f"{self._url}/previous")
    
    def set_volume_level(self, volume):
        # Home Assistant envoie 0.5 -> On convertit en 50 pour le Mac
        level = int(volume * 100)
        requests.put(f"{self._url}/volume", json={"level": level})
        self._volume = volume # Mise à jour immédiate pour l'interface
