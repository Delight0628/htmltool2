"""
页琢 - HTML 可视化编辑器 托盘服务
支持 PyInstaller 打包运行和普通 Python 运行两种模式。
"""
import os
import sys
import webbrowser
import threading
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import pystray
from PIL import Image

APP_NAME = "页琢"
APP_DESC = "页琢 HTML 可视化编辑器"


def _get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _get_bundle_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


BASE_DIR = _get_base_dir()
BUNDLE_DIR = _get_bundle_dir()

for _candidate in [BASE_DIR / "html", BASE_DIR, BUNDLE_DIR]:
    if (_candidate / "index.html").is_file():
        ROOT = _candidate
        break
else:
    ROOT = BASE_DIR

PORT = 8765
AUTO_OPEN = "--no-open" not in sys.argv


class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args, **kwargs):
        pass


def _serve():
    os.chdir(ROOT)
    server = HTTPServer(("127.0.0.1", PORT), SilentHandler)
    server.serve_forever()


def _open_url():
    webbrowser.open(f"http://127.0.0.1:{PORT}/index.html")


def _is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def _load_icon() -> Image.Image:
    for base in [BASE_DIR, BUNDLE_DIR]:
        for name in ["icon.ico", "icon.png"]:
            p = base / name
            if p.is_file():
                return Image.open(p)
    return Image.new("RGB", (64, 64), "#4a90d9")


def _restart(icon, _item):
    python = sys.executable
    os.execl(python, python, *sys.argv)


def _exit(icon, _item):
    icon.stop()
    os._exit(0)


def main():
    if _is_port_in_use(PORT):
        if AUTO_OPEN:
            _open_url()
        return

    threading.Thread(target=_serve, daemon=True).start()

    icon = pystray.Icon(
        APP_NAME,
        _load_icon(),
        f"{APP_DESC} (http://127.0.0.1:{PORT})",
        menu=pystray.Menu(
            pystray.MenuItem("打开编辑器", lambda i, it: _open_url()),
            pystray.MenuItem("重新启动", _restart),
            pystray.MenuItem("退出", _exit),
        ),
    )

    if AUTO_OPEN:
        _open_url()

    icon.run()


if __name__ == "__main__":
    main()
