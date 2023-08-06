# Copyright 2022 iiPython

# Modules
import os
import random
import secrets
from typing import Tuple
from requests import post
from threading import Thread
from types import FunctionType
from flask_socketio import SocketIO
from jinja2 import Environment, FileSystemLoader
from flask import Flask, abort, request, send_from_directory

from requests.exceptions import ConnectionError as CE

from .webpage import load_page

# Initialization
socketio_script = """<script src = "/_nitrostatic/js/socket.io.js"></script><script src = "/_nitrostatic/js/wrapper.js"></script>"""

# Flask app maker
def make_app(
    nitrogen,
    source_dir: str,
    use_jinja: bool,
    shutdown_token: str
) -> Tuple[Flask, SocketIO]:
    source_dir = os.path.abspath(source_dir)

    # Create flask app
    app = Flask("Nitrogen", template_folder = source_dir)  # Specifies template_folder for manual nitrogen.route calls
    sio = SocketIO(app)

    # Create Jinja env for templating
    env = Environment(loader = FileSystemLoader(source_dir))

    # Primary routes
    @app.route("/<path:path>", methods = ["GET"])
    def get_file(path: str) -> None:
        if path.split(".")[-1] in ["html", "html", "jinja"] and use_jinja:
            return socketio_script + "\n" + env.get_template(path).render({})

        return send_from_directory(source_dir, path, conditional = True)

    @app.route("/_nitrostatic/<path:path>", methods = ["GET"])
    def get_nitrogen_static(path: str) -> None:
        return send_from_directory(os.path.dirname(__file__), path, conditional = True)

    @app.route("/_initappshutdown", methods = ["POST"])
    def shutdown_app() -> None:
        if request.form.get("token", "") != shutdown_token:
            return abort(403)

        sio.stop()
        return "200 OK", 200

    return app, sio

# Nitrogen class
class Nitrogen(object):
    def __init__(
        self,
        source_dir: str = "src",
        use_jinja: bool = True
    ) -> None:
        self.source_dir = source_dir
        self.use_jinja = use_jinja

        # Generate runtime information
        self._runtime = {
            "port": random.randint(10000, 65535),
            "token": secrets.token_urlsafe(256)
        }

        # Create flask app
        self.app, self.sio = make_app(self, self.source_dir, self.use_jinja, self._runtime["token"])
        self.emit = self.sio.emit

    def on(self, event: str) -> FunctionType:
        def wrapper(cb: FunctionType) -> None:
            self.sio.on(event)(lambda a: cb(*a))

        return wrapper

    def stop(self) -> None:
        if not hasattr(self, "_runtime"):
            raise RuntimeError("Nitrogen was never started!")

        try:
            post(
                f"http://localhost:{self._runtime['port']}/_initappshutdown",
                data = {"token": self._runtime["token"]}
            )

        except CE:
            pass

        except Exception as e:
            print("[Nebula -] Failed to stop Flask server")
            raise e

        print("[Nebula +] Stopped Flask server")

    def route(self, rule: str, **options) -> FunctionType:
        return self.app.route(rule, **options)

    def start(self, start_location: str = "index.html", fullscreen: bool = False) -> None:

        # Launch Flask
        Thread(
            target = self.sio.run,
            args = [self.app],
            kwargs = {"host": "localhost", "port": self._runtime["port"]}
        ).start()
        print(f"[Nebula +] Launched Flask on LOCAL address http://localhost:{self._runtime['port']}")

        # Launch our Qt5 application
        load_page(f"http://localhost:{self._runtime['port']}/{start_location}", fullscreen)
        self.stop()
