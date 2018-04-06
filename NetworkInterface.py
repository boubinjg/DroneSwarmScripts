import os
import socket

PORT = 45453 #Standard
HOST = ''
CoAPCommand = ''
CoAPAddr = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT));
s.listen(10);

while 1:
        conn, addr = s.accept();
        print addr[0] + ':' + str(addr[1]);
        command = conn.recv(1024).split(',');
        print(command)
        if command[0] == "break":
            break;
        CoAPAddr = command[0];
        CoAPCommand = command[1]

        os.system("./coap-client -m put coap://"+CoAPAddr+":5117/cr -"+CoAPCommand);
        conn.send("Sent");
s.close()
