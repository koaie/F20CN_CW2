from server import Server
from concurrent.futures import ThreadPoolExecutor
import time

server = Server('127.0.0.1', 8888)
server.listen()

if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        while True:
            conn, addr = server.accept()
            executor.submit(server.connection, conn, addr)
            time.sleep(1)
