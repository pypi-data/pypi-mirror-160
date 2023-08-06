import socket


class ClientConnection:
    def __init__(self, ip="", port=4711):
        """Initializes from the IP and from the port."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    @staticmethod
    def connect(ip="", port=4711):
        """Shortcut for __init__"""
        return ClientConnection(ip, port)

    def send(self, what_to_send):
        if type(what_to_send) == str:
            what_to_send = bytes(what_to_send.encode('utf-8'))
        """Sends data to the server. Automatically adds a new line if there isn't one."""
        if not what_to_send.decode('utf-8').endswith("\n"):
            what_to_send += b"\n"
        self.socket.sendall(what_to_send)

    def recieve(self, how_much=1024):
        """Recieve how_much data from the server. 1024 by default. Automatically strips down the new line if there is one."""
        result = self.socket.recv(how_much)

        if result.decode('utf-8').endswith("\n"):
            return result[: len(result) - 1]
        else:
            return result

    def send_and_recieve(self, what_to_send, how_much=1024):
        """Sends what_to_send and recieves how_much."""
        self.send(what_to_send)
        return self.recieve(how_much)

    def disconnect(self):
        """Disconnects safely from the server."""
        self.socket.close()
