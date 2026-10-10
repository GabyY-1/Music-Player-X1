"""Music Player X1 - Windows-only GSMTC loopback companion.
Requires Python 3.10+ and `pip install winsdk`.
Exposes only the current Windows media session at 127.0.0.1.
"""
import asyncio
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

if sys.platform != "win32":
    raise SystemExit("Ce compagnon fonctionne uniquement sous Windows 10/11.")

try:
    from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager
except ImportError:
    raise SystemExit("Module manquant : installe winsdk avec : py -m pip install winsdk")

HOST = "127.0.0.1"
PORT = 8765
ALLOWED_ORIGINS = {
    "https://gabyy-1.github.io",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
}

def select_session(manager):
    sessions = list(manager.get_sessions())
    if not sessions:
        return None
    for session in sessions:
        try:
            status = str(session.get_playback_info().playback_status).lower()
            if "playing" in status or status == "4":
                return session
        except Exception:
            pass
    return manager.get_current_session() or sessions[0]

async def get_status():
    manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
    session = select_session(manager)
    if session is None:
        return {"session": None}
    props = await session.try_get_media_properties_async()
    info = session.get_playback_info()
    status = str(info.playback_status).split(".")[-1]
    return {"session": {
        "app": str(session.source_app_user_model_id or "Application"),
        "title": str(props.title or ""),
        "artist": str(props.artist or ""),
        "album": str(props.album_title or ""),
        "status": status
    }}

async def control(action):
    manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
    session = select_session(manager)
    if session is None:
        return False
    if action == "toggle":
        return bool(await session.try_toggle_play_pause_async())
    if action == "next":
        return bool(await session.try_skip_next_async())
    if action == "previous":
        return bool(await session.try_skip_previous_async())
    return False

class Handler(BaseHTTPRequestHandler):
    def origin(self):
        origin = self.headers.get("Origin", "")
        return origin if origin in ALLOWED_ORIGINS else None

    def common_headers(self):
        origin = self.origin()
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Private-Network", "true")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")

    def respond(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.common_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def authorized(self):
        # Requests without an Origin are allowed for command-line diagnostics.
        origin = self.headers.get("Origin")
        return origin is None or origin in ALLOWED_ORIGINS

    def do_OPTIONS(self):
        if not self.authorized():
            self.respond(403, {"error": "Origin non autorisée"})
            return
        self.send_response(204)
        self.common_headers()
        self.end_headers()

    def do_GET(self):
        if not self.authorized() or self.path != "/status":
            self.respond(403 if not self.authorized() else 404, {"error": "Accès refusé"})
            return
        try:
            self.respond(200, asyncio.run(get_status()))
        except Exception as exc:
            self.respond(503, {"error": type(exc).__name__})

    def do_POST(self):
        if not self.authorized() or self.path != "/control":
            self.respond(403 if not self.authorized() else 404, {"error": "Accès refusé"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size > 1024 or size <= 0:
                self.respond(400, {"error": "Taille invalide"})
                return
            payload = json.loads(self.rfile.read(size))
            action = payload.get("action")
            if action not in {"toggle", "next", "previous"}:
                self.respond(400, {"error": "Commande inconnue"})
                return
            self.respond(200, {"ok": asyncio.run(control(action))})
        except (ValueError, json.JSONDecodeError):
            self.respond(400, {"error": "Données invalides"})
        except Exception as exc:
            self.respond(503, {"error": type(exc).__name__})

    def log_message(self, fmt, *args):
        print("[X1]", fmt % args)

if __name__ == "__main__":
    print(f"Music Player X1 : compagnon Windows actif sur http://{HOST}:{PORT}")
    print("Ferme cette fenêtre ou utilise Ctrl+C pour arrêter.")
    try:
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nCompagnon arrêté.")
