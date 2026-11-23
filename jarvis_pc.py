# JARVIS PC Bridge (Windows). Sirf Python stdlib chahiye. Chalane ke liye: python jarvis_pc.py
import json, os, subprocess, ctypes, datetime, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 5050
# Sirf aapki apni website se aane do (apna GitHub Pages URL yahan daalo, jaise "https://username.github.io")
ALLOWED_ORIGINS = ["http://localhost", "http://127.0.0.1", "null", "https://*.github.io"]
MODELS = [
    "https://aiplatform.googleapis.com/v1/publishers/google/models/gemini-2.5-flash:generateContent",
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
]

def origin_ok(origin):
    if not origin: return True
    for a in ALLOWED_ORIGINS:
        if a == origin or (a.startswith("https://*.") and origin.startswith("https://") and origin.endswith(a[9:])):
            return True
        if origin.startswith(a + ":"): return True
    return False

def key_press(vk):
    u = ctypes.windll.user32
    u.keybd_event(vk, 0, 0, 0); u.keybd_event(vk, 0, 2, 0)

def do_action(action):
    if action == "calculator": subprocess.Popen("calc"); return "कैलकुलेटर खोल दिया।"
    if action == "notepad": subprocess.Popen("notepad"); return "नोटपैड खोल दिया।"
    if action == "chrome": subprocess.Popen("start chrome", shell=True); return "क्रोम खोल रहा हूँ।"
    if action == "paint": subprocess.Popen("mspaint"); return "पेंट खोल दिया।"
    if action == "vol_up":
        for _ in range(5): key_press(0xAF)
        return "आवाज बढ़ा दी।"
    if action == "vol_down":
        for _ in range(5): key_press(0xAE)
        return "आवाज कम कर दी।"
    if action == "vol_mute": key_press(0xAD); return "आवाज म्यूट कर दी।"
    if action == "lock": ctypes.windll.user32.LockWorkStation(); return "स्क्रीन लॉक कर रहा हूँ।"
    if action == "shutdown": subprocess.Popen("shutdown /s /t 30"); return "तीस सेकंड में कंप्यूटर बंद होगा। रोकने के लिए कहिए, शटडाउन रोको।"
    if action == "abort_shutdown": subprocess.Popen("shutdown /a"); return "शटडाउन रोक दिया।"
    if action == "screenshot":
        try:
            from PIL import ImageGrab
            folder = os.path.join(os.path.expanduser("~"), "Pictures")
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, "jarvis_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png")
            ImageGrab.grab().save(path)
            return "स्क्रीनशॉट Pictures फ़ोल्डर में सेव हो गया।"
        except ImportError:
            return "स्क्रीनशॉट के लिए पहले pip install pillow चलाइए।"
    return None

def ask_gemini(api_key, contents):
    key = api_key or os.environ.get("GEMINI_API_KEY", "")
    if not key: return None, "API key nahi mili"
    body = json.dumps({"contents": contents, "generationConfig": {"temperature": 0.7, "maxOutputTokens": 200}}).encode()
    last = ""
    for url in MODELS:
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "x-goog-api-key": key})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode())
            return data["candidates"][0]["content"]["parts"][0]["text"], None
        except urllib.error.HTTPError as e:
            last = e.read().decode(errors="ignore")[:300]
            print("[ASK ERROR]", url.split("/")[2], last)
        except Exception as e:
            last = str(e); print("[ASK ERROR]", last)
    return None, last

class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        origin = self.headers.get("Origin", "")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        if origin_ok(origin):
            self.send_header("Access-Control-Allow-Origin", origin or "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Private-Network", "true")
            self.send_header("Vary", "Origin")
        self.end_headers()
        self.wfile.write(json.dumps(obj, ensure_ascii=False).encode())

    def do_OPTIONS(self): self._send(204, {})
    def do_GET(self):
        if self.path == "/ping": self._send(200, {"status": "ok"})
        else: self._send(404, {"status": "error"})

    def do_POST(self):
        if not origin_ok(self.headers.get("Origin", "")):
            return self._send(403, {"status": "error", "error": "origin allowed nahi"})
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        except Exception:
            return self._send(400, {"status": "error", "error": "bad json"})
        if self.path == "/run":
            msg = do_action(data.get("action", ""))
            return self._send(200, {"status": "ok", "message": msg} if msg else {"status": "error", "error": "unknown action"})
        if self.path == "/ask":
            reply, err = ask_gemini(data.get("apiKey", ""), data.get("contents", []))
            return self._send(200, {"status": "ok", "reply": reply} if reply else {"status": "error", "error": err})
        self._send(404, {"status": "error"})

    def log_message(self, *a): pass

if __name__ == "__main__":
    print(f"JARVIS PC Bridge chal raha hai: http://127.0.0.1:{PORT}  (band karne ke liye Ctrl+C)")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
