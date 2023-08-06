import logging
logger = logging.getLogger(__name__)

from copy import deepcopy
import json
import socket

import zmq
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

class TCPServer:
    def __init__(self, *, server_endpoint, server_config, server_secret_key_filename, client_key_path):
        self.server_endpoint    = deepcopy(server_endpoint)
        self.server_config      = {} if server_config is None else deepcopy(server_config)
        self.server_secret_key_filename = server_secret_key_filename
        self.client_key_path    = client_key_path
        logger.info("TCPServer created")
        logger.info(f"    server_endpoint: {self.server_endpoint}")
        logger.info(f"    server_config: {self.server_config}")
        logger.info(f"    server_secret_key_filename: {self.server_secret_key_filename}")
        logger.info(f"    client_key_path: {self.client_key_path}")

    def get_client(self):
        server_endpoint = deepcopy(self.server_endpoint)
        ip = self.server_endpoint.get('ip')
        if ip is None:
            hostname = socket.gethostname()
            ip       = socket.gethostbyname(hostname)
            server_endpoint['ip'] = ip

        return "unicorncommon.channels.tcp.TCPClient", deepcopy(server_endpoint)

    def start_server(self, server, quit_requested):
        ip = self.server_endpoint.get('ip')
        endpoint = f"tcp://{'*' if ip is None else ip}:{self.server_endpoint['port']}"
        poll_timeout = self.server_config.get("poll_timeout", 15000) # 15 seconds
        with zmq.Context.instance() as context:
            auth = ThreadAuthenticator(context)
            try:
                auth.start()
                auth.allow()
                auth.configure_curve(domain='*', location=self.client_key_path)
                with context.socket(zmq.REP) as socket:
                    server_public, server_secret = zmq.auth.load_certificate(self.server_secret_key_filename)
                    socket.curve_publickey = server_public
                    socket.curve_secretkey = server_secret
                    socket.curve_server = True
                    socket.bind(endpoint)
                    while not quit_requested():
                        flags = socket.poll(timeout=poll_timeout)
                        if flags == 0:
                            # no message
                            server.on_idle()
                            continue

                        message = socket.recv()
                        request = json.loads(message.decode("utf-8"))
                        response = server.handle_request(request)
                        socket.send(json.dumps(response).encode("utf-8"))
                        server.on_idle()
            finally:
                auth.stop()


class TCPClient:
    def __init__(self, *, server_endpoint, client_config, server_public_key_filename, client_secret_key_filename):
        self.server_endpoint = deepcopy(server_endpoint)
        self.client_config = {} if client_config is None else deepcopy(client_config)
        self.server_public_key_filename = server_public_key_filename
        self.client_secret_key_filename = client_secret_key_filename
        logger.info("TCPClient created")
        logger.info(f"    server_endpoint: {self.server_endpoint}")
        logger.info(f"    client_config: {self.client_config}")
        logger.info(f"    server_public_key_filename: {self.server_public_key_filename}")
        logger.info(f"    client_secret_key_filename: {self.client_secret_key_filename}")

    def send(self, request):
        with zmq.Context() as context:
            client_public, client_secret = zmq.auth.load_certificate(self.client_secret_key_filename)
            server_public, _ = zmq.auth.load_certificate(self.server_public_key_filename)

            with context.socket(zmq.REQ) as socket:
                socket.curve_secretkey = client_secret
                socket.curve_publickey = client_public
                socket.curve_serverkey = server_public

                endpoint = f"tcp://{self.server_endpoint['ip']}:{self.server_endpoint['port']}"
                socket.connect(endpoint)

                message = json.dumps(request)
                socket.send(message.encode("utf-8"))

                message = socket.recv()
                response = json.loads(message.decode("utf-8"))
                return response
