import socket
from threading import Thread


class CommandServer:
    def __init__(self, ip="", port=4711, max_users=1024):

        # Create the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind it to the needed IP and port.
        self.socket.bind((ip, port))

        # TCP sockets need max user amounts.
        self.socket.listen(max_users)

        # Create an empty events dict.
        self.events = dict()

        self.clients = dict()

    def on(self, id_):
        """
        A decorator. ID is the module and function name separated by a dot.
        """
        # print(id_)
        # Actual decorator here
        def deco(func):
            self.events[id_] = func  # connect the event

            return func

        # print(self.events)
        return deco

    def _run(self):
        self.stopped = False
        while not self.stopped:
            client, ip = self.socket.accept()

            self.clients[ip] = Thread(
                target=self._client_handler, args=[client], daemon=True
            )
            self.clients[ip].start()

    def run(self):  # Copied from mycellium code.
        self.socket_thread = Thread(target=self._run, daemon=True)
        self.socket_thread.start()

    def _client_handler(self, client):
        self.stopped = False
        while not self.stopped:
            try:
                data = client.recv(4096).decode("utf-8")
                # print(data)
                command, args = data.split("(")
                args = args[: len(args) - 3].split(",")
                if command in self.events:
                    self.events[command](*args, data, client)

            except KeyboardInterrupt:
                self.stopped = False
                client.close()
