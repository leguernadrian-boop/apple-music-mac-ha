// Apple Music for Mac — companion server
// Runs on the Mac, bridges Music.app to Home Assistant via REST on port 8181.
//
// Setup:
//   1. npm install express
//   2. node server.js
//
// macOS permission required:
//   System Settings → Privacy & Security → Automation → enable Music under Terminal
//   Test: osascript -e 'tell application "Music" to get name of current track'
//
// Endpoints consumed by the HA integration (custom_components/apple_music/):
//   GET  /_ping        → { status: "ok" }  — used by config flow to verify connection
//   GET  /now_playing  → { player_state, name, artist, album, volume, speakers }
//   PUT  /play | /pause | /next | /previous  (no body)
//   PUT  /volume       body: { "level": <int 0–100> }

const express = require('express');
const { exec } = require('child_process');
const app = express();

app.use(express.json());

// Returns tab-separated fields so that quotes/backslashes in track metadata
// cannot corrupt the payload (avoids hand-building JSON inside AppleScript).
const NOW_PLAYING_SCRIPT = `
tell application "Music"
    if it is running then
        set tState to player state as text
        set tVol to sound volume
        set tName to ""
        set tArtist to ""
        set tAlbum to ""
        try
            set tName to name of current track
            set tArtist to artist of current track
            set tAlbum to album of current track
        end try
        return tState & tab & tVol & tab & tName & tab & tArtist & tab & tAlbum
    else
        return "stopped"
    end if
end tell
`;

// Returns comma-separated names of currently active AirPlay output devices.
const SPEAKERS_SCRIPT = `
tell application "Music"
    set d to {}
    repeat with dev in (get AirPlay devices)
        if current of dev is true then set end of d to name of dev
    end repeat
    set AppleScript's text item delimiters to ","
    return d as text
end tell
`;

// Required by config_flow.py — called during HA integration setup to verify the server is reachable.
app.get('/_ping', (req, res) => res.json({ status: 'ok' }));

app.get('/now_playing', (req, res) => {
    const trackPromise = new Promise(resolve =>
        exec(`osascript -e '${NOW_PLAYING_SCRIPT}'`, (err, out) => resolve({ err, out })));
    const speakerPromise = new Promise(resolve =>
        exec(`osascript -e '${SPEAKERS_SCRIPT}'`, (err, out) => resolve({ err, out })));

    Promise.all([trackPromise, speakerPromise]).then(([track, spk]) => {
        if (track.err) return res.json({ player_state: 'stopped' });
        const parts = track.out.trim().split('\t');
        if (parts.length < 5) return res.json({ player_state: parts[0] || 'stopped' });
        const [state, vol, name, artist, album] = parts;
        const speakers = (!spk.err && spk.out.trim()) ? spk.out.trim().split(',') : [];
        res.json({ player_state: state, name, artist, album, volume: parseInt(vol, 10) || 0, speakers });
    });
});

const music = (cmd) => (req, res) =>
    exec(`osascript -e 'tell application "Music" to ${cmd}'`, () => res.json({ status: 'ok' }));

app.put('/play',     music('play'));
app.put('/pause',    music('pause'));
app.put('/next',     music('next track'));
app.put('/previous', music('previous track'));

app.put('/volume', (req, res) => {
    const parsed = parseInt(req.body && req.body.level, 10);
    const lvl = Math.max(0, Math.min(100, isNaN(parsed) ? 0 : parsed));
    exec(`osascript -e 'tell application "Music" to set sound volume to ${lvl}'`, () =>
        res.json({ status: 'ok' }));
});

app.listen(8181, () => console.log('Apple Music bridge listening on :8181'));
