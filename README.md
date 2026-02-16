![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)
![version](https://img.shields.io/badge/version-2026.1.0-blue.svg)

# 🍎 Apple Music for Mac (Modern)
...# 🍎 Apple Music for Mac (Modern)

Cette intégration permet de contrôler Apple Music sur votre Mac directement depuis **Home Assistant**. 

### ✨ Fonctionnalités
* **Lecture / Pause / Suivant / Précédent** ⏯️
* **Contrôle du volume** en temps réel 🔊
* **Pochettes d'album HD** (via iTunes API) 🖼️
* **État de lecture** (Titre, Artiste, Album) 🎶

---

## 🛠️ 1. Prérequis sur le Mac

1. **Node.js** doit être installé sur votre Mac.
2. Créez un dossier `apple-music-modern` et placez-y le fichier `server.js` (code ci-dessous).
3. Installez Express dans ce dossier : `npm install express`.

### 🔐 Autorisations macOS (Étape Cruciale)
Pour que macOS autorise le partage des infos :
1. Allez dans **Réglages Système** > **Confidentialité et sécurité** > **Automatisation**.
2. Sous **Terminal**, cochez la case **Musique**.
3. Pour forcer la demande de permission, lancez cette commande :
   `osascript -e 'tell application "Music" to get name of current track'`

---

## 🚀 2. Installation de l'Intégration

### Via HACS
1. Ajoutez ce dépôt comme **Dépôt personnalisé** (Custom Repository) dans HACS.
2. Cliquez sur **Télécharger**.
3. **Redémarrez Home Assistant**.

### Configuration dans Home Assistant
1. Allez dans **Paramètres** > **Appareils et services** > **Ajouter l'intégration**.
2. Cherchez **Apple Music for Mac (Modern)**.
3. Entrez l'**adresse IP** de votre Mac et le port `8181`.

---

## 🖥️ 3. Code du Serveur (server.js)

Copiez ce code dans un fichier nommé `server.js` sur votre Mac et lancez-le avec `node server.js` :

```javascript
const express = require('express');
const { exec } = require('child_process');
const app = express();
app.use(express.json());

app.get('/now_playing', (req, res) => {
    const script = `
        tell application "Music"
            if it is running then
                set tName to name of current track
                set tArtist to artist of current track
                set tAlbum to album of current track
                set tVol to sound volume
                set tState to player state as text
                return "{\\"player_state\\": \\"" & tState & "\\", \\"name\\": \\"" & tName & "\\", \\"artist\\": \\"" & tArtist & "\\", \\"album\\": \\"" & tAlbum & "\\", \\"volume\\": " & tVol & "}"
            else
                return "{\\"player_state\\": \\"stopped\\"}"
            end if
        end tell
    `;
    exec(\`osascript -e '\${script}'\`, (error, stdout) => {
        try { res.send(JSON.parse(stdout.trim())); } 
        catch (e) { res.send({ player_state: "stopped" }); }
    });
});

app.put('/play', (req, res) => exec('osascript -e "tell application \\"Music\\" to play"', () => res.send({status:"ok"})));
app.put('/pause', (req, res) => exec('osascript -e "tell application \\"Music\\" to pause"', () => res.send({status:"ok"})));
app.put('/next', (req, res) => exec('osascript -e "tell application \\"Music\\" to next track"', () => res.send({status:"ok"})));
app.put('/previous', (req, res) => exec('osascript -e "tell application \\"Music\\" to previous track"', () => res.send({status:"ok"})));
app.put('/volume', (req, res) => {
    const vol = req.body.level;
    exec(\`osascript -e "tell application \\"Music\\" to set sound volume to \${vol}"\`, () => res.send({status:"ok"}));
});

app.listen(8181, () => console.log('Moteur Apple Music prêt sur 8181 !'));
