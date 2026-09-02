import http.server
import socketserver
import socket
import ssl
import os
import sys
import threading
import subprocess
import shutil

PORT = 8080
TLS_PORT = 8443
ROOT = os.path.dirname(os.path.abspath(__file__))
DIRECTORY = os.path.join(ROOT, 'Quarry', 'www')
CERT_DIR = os.path.join(ROOT, 'certs')
CERT_FILE = os.path.join(CERT_DIR, 'cert.pem')
KEY_FILE = os.path.join(CERT_DIR, 'key.pem')
ERROR_LOG = os.path.join(ROOT, 'error.log')


def log_exception(msg):
    try:
        with open(ERROR_LOG, 'a', encoding='utf-8') as f:
            f.write(msg.rstrip() + '\n')
    except Exception:
        pass


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        pass

    def log_error(self, format, *args):
        log_exception(f"[HTTP ERROR] {format % args}")

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, BrokenPipeError, TimeoutError, ssl.SSLError):
            pass
        except Exception as e:
            log_exception(f"[HANDLER EXCEPTION] {e}")

    def end_headers(self):
        # Force service worker and manifest to never be cached at the HTTP layer
        clean_path = self.path.split('?', 1)[0]
        if clean_path.endswith('sw.js') or clean_path.endswith('manifest.webmanifest') or clean_path.endswith('.html') or clean_path == '/':
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        super().end_headers()

    def do_POST(self):
        if self.path.split('?', 1)[0] == '/log':
            length = int(self.headers.get('Content-Length', '0') or 0)
            body = self.rfile.read(min(length, 16384)).decode('utf-8', 'replace')
            log_exception(body)
            self.send_response(204)
            self.end_headers()
            return
        self.send_error(404, 'File not found')


class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionResetError, BrokenPipeError, TimeoutError, ssl.SSLError)):
            return
        log_exception(f"[SERVER EXCEPTION] {exc}")


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def ensure_favicon():
    src = os.path.join(DIRECTORY, 'icon-192.png')
    dest = os.path.join(DIRECTORY, 'favicon.ico')
    try:
        if os.path.isfile(src) and not os.path.isfile(dest):
            shutil.copyfile(src, dest)
    except Exception as e:
        log_exception(f"[FAVICON] {e}")


def ensure_tls_cert(ip):
    os.makedirs(CERT_DIR, exist_ok=True)
    stamp = os.path.join(CERT_DIR, 'san.txt')
    san = f"DNS:localhost,IP:127.0.0.1,IP:{ip}"
    previous = ''
    if os.path.isfile(stamp):
        with open(stamp, 'r', encoding='utf-8') as f:
            previous = f.read().strip()
    if os.path.isfile(CERT_FILE) and os.path.isfile(KEY_FILE) and previous == san:
        return True
    openssl = shutil.which('openssl')
    if not openssl:
        log_exception('[TLS] openssl not found; HTTPS disabled')
        return False
    try:
        subprocess.run([
            openssl, 'req', '-x509', '-newkey', 'rsa:2048', '-sha256',
            '-days', '825', '-nodes',
            '-keyout', KEY_FILE, '-out', CERT_FILE,
            '-subj', '/CN=cat-app',
            '-addext', f'subjectAltName={san}'
        ], check=True, capture_output=True, text=True)
        with open(stamp, 'w', encoding='utf-8') as f:
            f.write(san)
        return True
    except Exception as e:
        log_exception(f"[TLS] {e}")
        return False


def serve(httpd):
    try:
        httpd.serve_forever()
    except Exception as e:
        log_exception(f"[SERVER EXCEPTION] {e}")


def start_server():
    os.chdir(ROOT)
    ensure_favicon()
    ip = get_ip()
    try:
        httpd = ThreadingHTTPServer(("", PORT), Handler)
    except Exception as e:
        log_exception(f"[SERVER EXCEPTION] {e}")
        sys.exit(1)

    print("cat-app Server running.")
    print(f"Mac URL:           http://127.0.0.1:{PORT}")
    print(f"iPad Safari URL:   http://{ip}:{PORT}")

    if ensure_tls_cert(ip):
        try:
            tls = ThreadingHTTPServer(("", TLS_PORT), Handler)
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            ctx.load_cert_chain(CERT_FILE, KEY_FILE)
            tls.socket = ctx.wrap_socket(tls.socket, server_side=True)
            threading.Thread(target=serve, args=(tls,), daemon=True).start()
            print(f"iPad HTTPS (PWA):  https://{ip}:{TLS_PORT}")
            print("Offline Home Screen: open the HTTPS URL, accept the cert warning once, then Share → Add to Home Screen.")
        except Exception as e:
            log_exception(f"[TLS] {e}")
            print("HTTPS unavailable; HTTP will still serve the game.")
    sys.stdout.flush()
    serve(httpd)


if __name__ == '__main__':
    start_server()
