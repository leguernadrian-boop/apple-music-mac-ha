# 🍎 Apple Music for Mac (Modern)

![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)
![version](https://img.shields.io/badge/version-2026.1.0-blue.svg)
![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)

Apple Music for Mac (Modern) est une intégration fluide et élégante pour contrôler votre musique directement depuis votre tableau de bord **Home Assistant**.

---

## 🧐 Qu'est-ce que c'est ?
Cette intégration fait le pont entre votre Mac et Home Assistant. Elle vous permet non seulement de piloter la lecture, mais aussi d'afficher des informations riches comme les pochettes d'album en haute définition.

### ✨ Fonctionnalités
* 🛠 **Contrôle complet** : Lecture, Pause, Suivant, Précédent.
* 🔊 **Gestion du volume** : Réglage précis du son de l'application Musique.
* 🖼 **Artwork HD** : Récupération automatique de la pochette via iTunes API.
* 🎶 **Infos Live** : Titre, Artiste et Album mis à jour en temps réel.
* 🚀 **Zéro latence** : Communication directe via un serveur local léger.

---

## 🛠 Installation

### 1️⃣ Prérequis sur le Mac
1. **Node.js** doit être installé sur votre machine.
2. Créez un dossier nommé `apple-music-modern`.
3. Installez le serveur : `npm install express`.

### 2️⃣ Installation dans Home Assistant
* **Via HACS** : Ajoutez ce dépôt en tant que *Custom Repository*.
* **Téléchargement** : Cliquez sur installer et **redémarrez Home Assistant**.
* **Configuration** : Allez dans *Paramètres* → *Appareils et services* → *Ajouter l'intégration*.

---

## 🖥️ Configuration du Serveur (Mac)

Pour que l'intégration fonctionne, le fichier `server.js` doit tourner sur votre Mac. 

1. Copiez le code suivant dans votre fichier `server.js`.
2. Lancez-le avec la commande : `node server.js`

<details>
<summary>👉 Cliquez pour voir le code du serveur</summary>

```javascript
// [Insère ici ton code server.js version AppleScript que nous avons validé]
</details>

🔐 Autorisations macOS
[!IMPORTANT]
Pour que le serveur puisse lire les infos de Musique, vous devez donner une autorisation :

Réglages Système → Confidentialité et sécurité → Automatisation.

Cochez la case Musique sous l'application Terminal.

Si besoin, lancez : osascript -e 'tell application "Music" to get name of current track'

❓ Troubleshooting
L'entité est indisponible ? Vérifiez que le serveur node tourne sur le port 8181.

Le volume ne bouge pas ? Assurez-vous d'avoir bien donné les droits d'Automatisation.

Pas d'image ? L'image nécessite une connexion internet pour interroger l'API iTunes.

🤝 Crédits
Développé par @adrianleguern.
Inspiré par la communauté Home Assistant et le besoin d'une intégration macOS moderne.


---
