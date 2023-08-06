from argparse import Namespace
from unittest import TestCase

from ..scln_client import SclnClient, SclnClientError
from ..scln_client import get_args

import threading
import socket


class GetArgsTest(TestCase):
    def setUp(self) -> None:
        self.host = "127.0.0.1"
        self.port = "40000"
        self.args_list = ["--host", self.host, "--port", self.port]

    def test_args(self):
        args = get_args(arguments=self.args_list)
        self.assertIsInstance(args, Namespace)
        self.assertEqual(args.host, self.host)
        self.assertEqual(args.port, int(self.port))

    def test_empty_args(self):
        self.assertRaises(SystemExit, get_args, [])


class SclnClientTest(TestCase):
    def run_fake_server(self):
        # Run a server to listen for a connection and then close it
        server_sock = socket.socket()
        server_sock.bind(("127.0.0.1", 7777))
        server_sock.listen(0)
        server_sock.accept()
        server_sock.close()

    def setUp(self) -> None:
        server_thread = threading.Thread(target=self.run_fake_server)
        server_thread.start()

        self.client = SclnClient("127.0.0.1", 7777)
        self.client.close()

        server_thread.join()

    def test_run_client_terminal(self):
        server_thread = threading.Thread(target=self.run_fake_server)
        server_thread.start()

        self.client = SclnClient("127.0.0.1", 7777)
        with self.assertRaises(SclnClientError):
            self.client.send_command(
                "HOLA", timeout=0.5, max_reconnect_on_message=1, max_tx_retries=1
            )
        self.client.close()

        server_thread.join()
