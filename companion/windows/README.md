# Compagnon Windows – Music Player X1

Permet de voir et de contrôler **les sessions multimédias que Windows expose**, et non toutes les applications sans exception. Compatible avec Windows 10/11 lorsque l'application musicale publie une session GSMTC.

## Installer

1. Installe **Python 3.10 ou plus récent** depuis le site officiel python.org si nécessaire.
2. Ouvre PowerShell dans ce dossier.
3. Lance `py -m pip install winsdk`.
4. Lance `py companion.py` et laisse la fenêtre ouverte.
5. Ouvre Music Player X1 dans **Chrome ou Edge sur le même PC Windows** et clique **Connecter le compagnon**.
6. Si le navigateur demande l'autorisation d'accéder au réseau local, accepte pour ce site.

Tu peux tester l'état du serveur local en ouvrant `http://127.0.0.1:8765/status` sur cet ordinateur.

## Attention

- Le programme ne se connecte pas à Spotify ou Deezer via ton compte, il interroge Windows.
- Certaines applications n'exposent pas les titres ou refusent les commandes.
- Le compagnon ne fonctionne pas sur ChromeOS, Android ou iOS.
- Le serveur écoute **uniquement** sur `127.0.0.1`. Il n'envoie pas tes données musicales sur internet.
- La connexion entre un site HTTPS et localhost peut être bloquée par le navigateur (permissions d'accès local ou sécurité des requêtes réseau privées); dans ce cas, essaie avec la version installée / le site hébergé, Chrome ou Edge et vérifie les permissions.
- Seules les origines du GitHub Pages officiel et des serveurs de développement listées dans le script ont accès depuis le navigateur. Pour un autre hébergeur, ajoute explicitement son origine HTTPS dans `ALLOWED_ORIGINS`.
- Aucun accès Bluetooth AVRCP aux données des autres appareils n'est fourni ici : associer un casque Bluetooth permet seulement de choisir une **sortie audio** compatible.
