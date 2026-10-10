# Music Player X1

Lecteur musical web et PWA, conçu pour ChromeOS, Windows et Android. Le lecteur accepte des fichiers audio choisis par l'utilisateur (formats dépendants du navigateur), joue les morceaux, propose favoris, file d'attente, recherche et commandes multimédias, et fonctionne hors ligne après première ouverture.

## Démarrer

Héberger ces fichiers sur GitHub Pages, Vercel, Netlify ou un serveur HTTPS. Pour un test local, utiliser un serveur HTTP (par exemple `python -m http.server 8000`). Ouvrir le site, cliquer sur **Ajouter des musiques**, sélectionner les fichiers. La bibliothèque locale est enregistrée dans IndexedDB quand le navigateur le permet. Aucune piste audio n'est envoyée à un serveur.

## Déploiement GitHub Pages

Dans Settings > Pages, choisir **Deploy from a branch**, branche `main` et dossier `/ (root)`. L'adresse devient `https://gabyy-1.github.io/Music-Player-X1/` une fois le déploiement terminé.

## Limitations importantes

Une PWA ne peut pas surveiller les musiques jouées par Deezer, Spotify, YouTube Music ou d'autres applications, ni lire les métadonnées AVRCP via Bluetooth classique. Une extension ne résout pas l'accès universel aux autres applications. Sur Windows, un futur compagnon natif peut utiliser **GlobalSystemMediaTransportControlsSessionManager** (GSMTC) pour les sessions exposées par les applications. Sur Android, une application native peut utiliser **MediaSessionManager** avec autorisation d'accès aux notifications quand les sessions sont exposées. Disponibilité, contrôle et artwork varient selon l'application et l'OS. Sur Chromebook une PWA seule n'accède pas aux sessions média système.

Les fichiers audio sélectionnés sont stockés localement via IndexedDB, sous réserve des quotas; le navigateur peut supprimer les données du site, il faut conserver les originaux. Certains navigateurs ne prennent pas en charge FLAC ou des codecs particuliers. Le mode PWA nécessite HTTPS (ou localhost); le service worker ne met en cache que le code de l'application, pas les bibliothèques audio de tiers.

## Licence

Code de départ du lecteur. Ajouter une licence adaptée avant publication et redistribution.

## Lectures des applications externes (Windows)
`companion/windows/companion.py` lit les sessions Windows GSMTC et les expose **uniquement à l'ordinateur local** sur `127.0.0.1:8765`. Voir `companion/windows/README.md`. Les apps doivent exposer leurs sessions à Windows; Deezer, Spotify et les navigateurs peuvent se comporter différemment suivant la version. Le navigateur peut bloquer une connexion depuis une PWA HTTPS vers localhost selon ses règles de sécurité; tester sur Chrome/Edge et autoriser l'accès local si demandé.

## Bluetooth
Le bouton **Choisir la sortie audio** utilise `navigator.mediaDevices.selectAudioOutput()` et `HTMLMediaElement.setSinkId()` si disponibles. Associer le casque/l'enceinte dans Windows ou ChromeOS avant de sélectionner la sortie. Ce n'est **pas** une connexion AVRCP, ni une capture universelle de métadonnées Bluetooth.
