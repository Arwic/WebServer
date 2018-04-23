import socket
from threading import Thread
import os

'''
GET / HTTP/1.1
Host: localhost
'''


def handle_request(conn, req):
    if req is None:
        print("Empty Request")
        return
    if req["uri"] == "/":
        req["uri"] = "/index.html"
    req["uri"] = req["uri"][1:]
    base_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(base_dir, "www", req["uri"])
    with open(file_path, "rb") as f:
        file_data = f.read()
        print(file_data)
        conn.send(file_data)


def parse_request(inp):
    try:
        lines = inp.split('\n')
        req = dict()
        req_line = lines[0].split(' ')
        req["method"] = req_line[0].rstrip()
        req["uri"] = req_line[1].rstrip()
        req["version"] = req_line[2].rstrip()
        req["Host"] = lines[1].split(':')[1].rstrip()[1:]
        print("Good request:", req)
        return req
    except:
        print("Bad request: ", inp)


def handle_client(conn, ip, port):
    active = True
    while active:
        raw_inp = conn.recv(5012)
        inp = raw_inp.decode("utf8").rstrip()
        '''if "--QUIT--" in inp:
            print("Client", ip, ":", port, "has requested to quit")
            conn.close()
            print("Client", ip, ":", port, "connection closed")
            active = False
        else:'''
        req = parse_request(inp)
        handle_request(conn, req)


def main():
    host = "localhost"
    port = 80

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((host, port))
    except:
        print("Unable to bind to port", port)
        exit(1)

    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        ip, port = str(addr[0]), str([addr[1]])
        print("New connection from", ip, ":", port)

        try:
            Thread(target=handle_client, args=(conn, ip, port)).start()
        except:
            print("Error creating new thread for client", ip, ":", port)

if __name__ == "__main__":
    main()
