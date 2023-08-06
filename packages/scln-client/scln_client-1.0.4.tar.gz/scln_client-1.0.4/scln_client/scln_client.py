#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Diego Gomez, Simon Torres"
__copyright__ = "Copyright 2019, SclnClient"
__credits__ = ["Diego Gomez", "Simon Torres"]
__license__ = "GPL"
__maintainer__ = "Diego Gomez"
__email__ = "diego.gomez@noirlab.edu, simon.torres@noirlab.edu"
__status__ = "Development"
__name__ = "SOAR Communication Library New Client"

"""
SclnClient
SOAR communication library new client

Procedures for SOAR TCS Communications
The command protocol is client/server with immediate response. A response should be never take longer than 1500 ms.
"""

import sys

import argparse
import socket
import logging
import threading

from argparse import Namespace
from importlib.metadata import version
from importlib.metadata import PackageNotFoundError
from time import sleep
from typing import Union, Callable

try:
    __version__ = version("scln_client")
except PackageNotFoundError:
    pass


class SclnClientError(Exception):
    """SclnClientError is a class that inherits from the Exception class."""

    pass


class SclnClient(object):
    """It creates a socket, connects to the host and port, and if it fails, it calls the reconnect function"""

    def __init__(
        self,
        host: str,
        port: int,
        timeout: float = 1.5,
        max_tx_retries: int = 12,
        max_rx_retries: int = 3,
        max_reconnect_attempts: int = 0,
        max_reconnect_on_message: int = 5,
        on_change: Callable = lambda x: x,
        connect_on_create=True,
    ):
        """
        It creates a socket, connects to the host and port, and if it fails, it calls the reconnect
        function

        :param host: The hostname or IP address of the server
        :param port: The port to connect to
        :param timeout: The time to wait for a response from the server before giving up
        :param max_tx_retries: The number of times to try sending a command before giving up, default to 12 (optional)
        :param max_rx_retries: The number of times to try to reconnect while receiving a message before giving up,
                               defaults to 3 (optional)
        :param max_reconnect_attempts: The number of times it will try to reconnect to the socket, if set to -1 it will
                                       try forever
        :param max_reconnect_on_message: The number of times it will try to reconnect to the socket if disconnect in
                                         middle of a message
        :param on_change: a function that will be called when the connection status changes
        :param connect_on_create: The flag to decide if connect on instantiation
        """
        self._socket = socket.socket()
        self._host = host
        self._port = port
        self._timeout = timeout
        self._max_tx_retries = max_tx_retries
        self._max_rx_retries = max_rx_retries
        self._max_reconnect_attempts = max_reconnect_attempts
        self._max_reconnect_on_message = max_reconnect_on_message
        self._on_change = on_change
        self._connected = False
        self._logger = logging.getLogger()
        self._lock = threading.Lock()
        if connect_on_create:
            self.connect(self._max_reconnect_attempts)

    def connect(self, max_attempts: int = 0) -> bool:
        """
        It attempts to reconnect to the socket, and if it fails, it waits 5 seconds and tries again.

        :param attempts: The number of times it will try to reconnect to the socket, if set to 0 it will try forever.
        :return: The return value is a boolean value.
        """
        try:
            self._socket = socket.socket()
            self._logger.info(f"Connecting to {self._host}:{self._port}")
            self._socket.settimeout(self._timeout)
            self._socket.connect((self._host, self._port))
            self._connected = True
            self._logger.info("Successfully connected")
            self._on_change(True)
            return True
        except TimeoutError:
            self._logger.error(
                f"Timeout error while connecting to {self._host}:{self._port}"
            )
            self.close()
            del self._socket
            if max_attempts > 0:
                sleep(5)
                self.connect(max_attempts - 1)
            elif max_attempts == -1:
                sleep(5)
                self.connect(max_attempts)
            else:
                raise SclnClientError(
                    f"Error connecting to {self._host}:{self._port} after multiple attempts"
                )
        except socket.error as e:
            raise SclnClientError(
                f"Error {str(e)} trying to connect to {self._host}:{self._port}"
            )

    @property
    def is_connected(self) -> bool:
        """
        It checks if the client is connected to the server.
        :return: The return value is a boolean value.
        """
        return self._connected

    def _transmit(self, cmd: str) -> bool:
        """
        It takes a string, converts it to bytes, prepends the length of the string to the bytes, and
        sends it over a socket

        :param cmd: The command to send to the server
        :return: The return value is a boolean.
        """
        size = (len(cmd)).to_bytes(4, byteorder="big")
        cmd_bytes = bytes(cmd, "ascii")
        try:
            self._socket.send(size + cmd_bytes)
            return True
        except socket.error:
            return False

    def _receive(self, timeout: float):
        """
        It receives a message from the socket, and if it's incomplete, it waits 0.5 seconds and tries
        again

        :param timeout: The time to wait for a response from the server
        :return: The data received from the socket.
        """
        try:
            self._socket.settimeout(timeout)
            size = self._socket.recv(4)
            full_size = int.from_bytes(size, byteorder="big", signed=False)
            data = self._socket.recv(full_size)
            data = bytes.decode(data)
            if len(data) != full_size:
                for i in range(self._max_rx_retries):
                    self._logger.debug(
                        f"Incomplete block, sleep 0.5s and retry - Attempt {i + 1}"
                    )
                    sleep(0.5)
                    aux_data = self._socket.recv(full_size - len(data))
                    aux_data = bytes.decode(aux_data)
                    data += aux_data
                    if len(data) == full_size:
                        break
                else:
                    raise SclnClientError(
                        f"Incomplete block received after {self._max_rx_retries} attempts"
                    )
        except socket.timeout:
            raise SclnClientError("Socket timeout error")
        return data

    def send_command(self, cmd: str, timeout: Union[float, None] = None):
        """
        It tries to send a command to the socket, if it fails it tries to reconnect to the socket and
        then tries to send the command again

        :param cmd: The command to send to the socket
        :param timeout: The timeout for the socket to receive a response, defaults to self._timeout (optional)
        :return: The response from the socket.
        """
        if timeout is None:
            timeout = self._timeout
        try:
            if float(timeout) <= 0:
                self._logger.error(
                    f"Timeout should be a number greater than 0, setting it to {self._timeout}"
                )
                timeout = self._timeout
            else:
                timeout = float(timeout)
        except ValueError:
            self._logger.error(f"Timeout is not a number, setting to {self._timeout}")
            timeout = self._timeout
        max_reconnect = False
        self._lock.acquire()
        if not self._connected:
            self._lock.release()
            raise SclnClientError(f"Socket still disconnected - command {cmd}")
        for i in range(self._max_tx_retries):
            try:
                self.clear_socket()
                sleep(0.05)
                if not self._transmit(cmd):
                    self._logger.error(f"Tx Socket Error - command {cmd}")
                    raise SclnClientError("Socket Error Transmitting")
                resp = self._receive(timeout)
                if resp is None:
                    self._logger.error(f"Rx Socket Timeout - command {cmd}")
                    raise SclnClientError("Socket Timeout Receiving")
                if resp == "":
                    self._logger.error(f"Empty socket response - command {cmd}")
                    raise SclnClientError("Empty socket response")
                break
            except SclnClientError:
                try:
                    self._socket.send(b"a")
                except socket.error as e:
                    self._logger.error(
                        f"Broken socket connection {str(e)}, reconnecting"
                    )
                    self._on_change(False)
                    self._connected = False
                    self._connected = self.connect(
                        attempts=self._max_reconnect_on_message
                    )
                    if not self._connected:
                        max_reconnect = True
                        break
        else:
            self._lock.release()
            raise SclnClientError(
                f"Error after retrying {self._max_tx_retries} times sending command - command {cmd}"
            )

        if max_reconnect:
            self._lock.release()
            raise SclnClientError(
                f"Error after trying to reconnect {self._max_reconnect_on_message} "
                f"times to socket - command {cmd}"
            )
        self._lock.release()
        return resp

    def clear_socket(self) -> None:
        """
        It sets the socket timeout to 0.05 seconds, then tries to read from the socket until it times
        out
        """
        self._socket.settimeout(0.05)
        try:
            while True:
                discard_buffer = self._socket.recv(1024)
                if len(discard_buffer) < 1024:
                    break
        except socket.error:
            pass

    def close(self) -> None:
        """
        It tries to close the socket, and if it fails, it logs an error
        """
        try:
            self._socket.close()
        except socket.error:
            self._logger.error("Error closing socket")

    def __str__(self):
        """
        The function returns a string that contains the host and port of the socket
        :return: The string representation of the object.
        """
        return f"Scln socket to {self._host}:{self._port}"

    def __repr__(self):
        """
        `__repr__` is a special method that returns a string representation of an object
        :return: The host and port of the SclnClient object.
        """
        return f"SclnClient({self._host}, {self._port})"


def get_args(arguments: Union[list, None] = None) -> Namespace:
    parser = argparse.ArgumentParser(
        description=f"Extracts goodman spectra and does automatic wavelength "
        f"calibration."
        f"\n\nCurrent Version: {__version__}"
    )

    parser.add_argument(
        "--host",
        action="store",
        type=str,
        dest="host",
        help="String with tcp/ip socket host",
    )

    parser.add_argument(
        "--port",
        action="store",
        type=int,
        dest="port",
        help="Number with tcp/ip socket port",
    )

    parser.add_argument(
        "--timeout",
        action="store",
        type=float,
        default=1.5,
        dest="timeout",
        help="Default timeout",
    )

    parser.add_argument(
        "--max-rx-retries",
        action="store",
        type=int,
        default=3,
        dest="max_rx_retries",
        help="Number of attempts to receive a message",
    )

    parser.add_argument(
        "--max-tx-retries",
        action="store",
        type=int,
        default=12,
        dest="max_tx_retries",
        help="Number of attempts to send a message",
    )

    parser.add_argument(
        "--max-reconnect-attempts",
        action="store",
        type=int,
        default=0,
        dest="max_reconnect_attempts",
        help="Number of attempts to connect the TCP socket",
    )

    parser.add_argument(
        "--max-reconnect-on-message",
        action="store",
        type=int,
        default=5,
        dest="max_reconnect_on_message",
        help="Number of attempts to reconnect while receiving a message",
    )

    parser.add_argument(
        "--connect-on-create",
        action="store",
        type=bool,
        default=True,
        dest="connect_on_create",
        help="Flag to decide if connect on instantiation of TcsClient",
    )

    args = parser.parse_args(args=arguments)

    if args.host is None or args.port is None:
        parser.print_help()
        sys.exit(0)

    return args


def run_client_terminal(arguments: Union[list, None] = None):
    """
    Function that runs a client terminal that allows the user to send
    commands to the Scln server
    """
    log = logging.getLogger()
    args = get_args(arguments=arguments)

    log.info("Creating SclnClient instance")
    scln = SclnClient(
        args.host,
        int(args.port),
        timeout=args.timeout,
        max_tx_retries=args.max_tx_retries,
        max_rx_retries=args.max_rx_retries,
        max_reconnect_attempts=args.max_reconnect_attempts,
        max_reconnect_on_message=args.max_reconnect_on_message,
        connect_on_create=args.connect_on_create,
    )

    try:
        while True:
            scln.clear_socket()
            cmd = input("Enter a command:\n>> ")
            if cmd.startswith("exit") or cmd.startswith("quit") or cmd == "q":
                scln.close()
                print("Goodbye")
                sys.exit(0)
            if cmd != "":
                print(f"<< {scln.send_command(cmd)}")
    except KeyboardInterrupt:
        print("Goodbye")
        sys.exit(0)
