<div align="center">
  <img src="logo.png" width="200" alt="Logo Apple Music">
</div>

# 🍎 Apple Music for Mac (Modern)

![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)
![version](https://img.shields.io/badge/version-2026.1.0-blue.svg)
![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)

A Home Assistant integration that bridges your Mac's Music app to your dashboard — playback control, live track info, HD album art, and AirPlay speaker detection.

---

## ✨ Features

- 🛠 **Full control** — Play, Pause, Next, Previous
- 🔊 **Volume** — Precise control of Music.app volume
- 🖼 **HD artwork** — Album art fetched automatically via iTunes API
- 🎶 **Live info** — Track, Artist, Album updated in real time
- 📡 **AirPlay speakers** — Shows which AirPlay outputs are currently active
- 🚀 **Local only** — Direct communication via a lightweight local server, no cloud

---

## 🛠 Installation

### 1. Mac companion server

The integration requires a small Node.js server running on your Mac that bridges Music.app over HTTP.

**Prerequisites:** Node.js installed on the Mac ([nodejs.org](https://nodejs.org) or `brew install node`)

```bash
# Create a folder for the server
mkdir ~/apple-music-bridge && cd ~/apple-music-bridge

# Copy server.js from this repo into that folder, then:
npm install express
node server.js
# → "Apple Music bridge listening on :8181"
```

**macOS permission (required):**

Go to **System Settings → Privacy & Security → Automation** and enable **Music** under Terminal (or whichever app runs the server). Without this, every osascript call silently fails.

To verify: `osascript -e 'tell application "Music" to get name of current track'`

**Keep it running across reboots** using a launchd plist (`~/Library/LaunchAgents/`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.apple-music-bridge</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/node</string>
        <string>/Users/YOUR_USERNAME/apple-music-bridge/server.js</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.apple-music-bridge.plist
```

### 2. Home Assistant integration (via HACS)

1. HACS → **Custom Repositories** → add `leguernadrian-boop/apple-music-mac-ha` → category: **Integration**
2. Install and **restart Home Assistant**
3. **Settings → Devices & Services → Add Integration** → search **Apple Music**
4. Enter your Mac's IP address and port `8181`

---

## 🔌 Server API reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/_ping` | Health check — called by HA during setup to verify connection |
| GET | `/now_playing` | Current playback state, track info, volume, active AirPlay speakers |
| PUT | `/play` | Start playback |
| PUT | `/pause` | Pause playback |
| PUT | `/next` | Next track |
| PUT | `/previous` | Previous track |
| PUT | `/volume` | Set volume — body: `{ "level": 0–100 }` |

**`/now_playing` response:**
```json
{
  "player_state": "playing",
  "name": "Track Title",
  "artist": "Artist Name",
  "album": "Album Name",
  "volume": 75,
  "speakers": ["Kitchen", "Living Room"]
}
```

`player_state` values: `"playing"` / `"paused"` / `"stopped"`

---

## 🤝 Credits

Developed by [@adrianleguern](https://github.com/leguernadrian-boop).  
Inspired by the need for a modern macOS integration for Home Assistant.
