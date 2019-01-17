import socket, gzip, ssl, os, logging, subprocess


class SockSsl:

    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        except socket.error:
            subprocess.Popen(['notify-send', "Сould not create socket"])
            logging.error("Socket creation error")
            exit(1)
        try:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        except ssl.SSLEOFError:
            subprocess.Popen(['notify-send', "SSL context loading failed"])
            logging.error("Fake context")
            exit(1)
        try:
            path = str(os.getcwd()) + "/credentials/Server/"
            self.context.check_hostname = True
            self.context.verify_mode = ssl.CERT_REQUIRED
            self.context.load_cert_chain(certfile=path + "crt.pem", keyfile=path + "key.pem")
            self.context.load_verify_locations(capath=path+"csr.pem")
            self.context.options |= ssl.PROTOCOL_TLSv1_2 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
            self.context.set_ciphers("TLS13+CDH+AESGCM:ECDH+CHACHA20")
        except ssl.SSLEOFError:
            subprocess.Popen(['notify-send', "Braking cert-chain"])
            logging.error("Corrupted cert-chain")
            exit(1)
        try:
            self.ssl_sock = self.context.wrap_socket(self.sock, server_side=True, do_handshake_on_connect=True)
        except ssl.SSLEOFError:
            subprocess.Popen(['notify-send', "Error of ssl-socket wrapping"])
            logging.error("Error loading cert-chain")
            exit(1)
        try:
            self.port = 4547
            self.host = "127.0.0.1"
            self.ssl_sock.bind((self.host, self.port))
        except OSError:
            subprocess.Popen(['notify-send', "Error of binding"])
            logging.error("Error of binding")
            exit(1)
        self.peer = "localhost"
        self.peername = "localhost"  # test version

    def con(self):
        self.ssl_sock.listen(1)
        c, p = self.ssl_sock.accept()
        if c != self.host:
            try:
                subprocess.check_call(["ufw", "deny", "incoming", "from", str(c)])
                logging.warning("Firewall role succefully added: %s (incoming traffic has blocked)" % str(c))
            except subprocess.CalledProcessError:
                logging.warning("Firewall role is not added!")
                exit(1)

    def send(self, data):
        _buf = gzip.compress(str(data), compresslevel=9)
        try:
            self.ssl_sock.send(_buf)
        except socket.error:
            subprocess.Popen(['notify-send', "Warning: sending metrics error"])
            exit(1)

    def __del__(self):
        self.ssl_sock.close()
        del self.ssl_sock, self.context, self.port, self.host, self.peer, self.peername
