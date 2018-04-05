import socket

HOST = "127.0.0.1";
PORT = 45455;

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect((HOST, PORT));
s.send("192.168.2.21,edn=DroneGimbalDriver-dc=shk");
s.send("break");
