"""
Copyright (c) Timothy Ings <tim@tim-ings.com>
All Rights Reserved
"""

import socket
from threading import Thread
import os
import re

SERVER_HOST = "localhost"
SERVER_PORT = 80
WWW_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "www")


def serve_static(conn, req):
    # send the requested file to the client
    file_path = os.path.join(WWW_DIR, req["uri"])
    with open(file_path, "rb") as f:
        conn.send(f.read())


def view_index(conn, req):
    file_path = os.path.join(WWW_DIR, "index.html")
    with open(file_path, "rb") as f:
        conn.send(f.read())


def ajax_echo(conn, req):
    conn.send(req["Content"].encode())


def form_echo(conn, req):
    conn.send(req["Content"].encode())

urlpatterns = [
    ("^ajax/echo$", ajax_echo),
    ("^static/", serve_static),
    ("^index/$", view_index),
    ("^form/echo", form_echo),
    ("^favicon.ico$", serve_static),
    ("^$", view_index),
]


def handle_request(conn, req):
    if req is None:
        return
    # trim leading "/"
    if len(req["uri"]) > 0 and req["uri"][0] == "/":
        req["uri"] = req["uri"][1:]
    # execute the view associated with the requested url
    for pattern in urlpatterns:
        if re.match(pattern[0], req["uri"]):
            pattern[1](conn, req)
            break


def parse_request(inp):
    if inp == "":
        return
    lines = inp.split('\r\n')
    req = {}
    # parse the request line
    http_req = lines[0].split(' ')
    req["method"] = http_req[0]
    req["uri"] = http_req[1]
    req["version"] = http_req[2]
    lines.pop(0)  # remove the http header so we dont parse it again

    # check for content
    if lines[-2] == "":
        lines.pop(-2)
        req["Content"] = lines.pop(-1)

    # parse the rest of the header
    for i in range(len(lines)):
        s = lines[i].split(":")
        k = s[0].strip()
        v = s[1].strip()
        req[k] = v
    print(http_req)
    return req


def handle_client(conn, ip, port):
    # receive data from the client, parse it, and then handle it
    raw_inp = conn.recv(5012)
    inp = raw_inp.decode("utf8").rstrip()
    req = parse_request(inp)
    handle_request(conn, req)
    conn.close()


def main():
    # create and bind a new socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((SERVER_HOST, SERVER_PORT))
    except:
        print("Unable to bind to port", SERVER_PORT)
        exit(1)

    # start listening for new clients
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        ip, port = str(addr[0]), str([addr[1]])
        print("New connection from", ip, ":", port)
        # hand the client off to a new thread
        try:
            Thread(target=handle_client, args=(conn, ip, port)).start()
        except:
            print("Error creating new thread for client", ip, ":", port)

if __name__ == "__main__":
    main()
