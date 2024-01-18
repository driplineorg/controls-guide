#! /usr/bin/env python 

import socket
import time

class SCPIClient:
    def __init__(self, host, port, ending='\n'):
        self.host = host
        self.port = port
        self.ending = ending

    def query(self, command):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        print(f'Connected to device at {self.host}:{self.port}')

        command += self.ending
        client_socket.send(command.encode('utf-8'))

        data = ''
        while True:
            data += client_socket.recv(1024).decode('utf-8')
            if data.endswith(self.ending):
                break
        return data

 
if __name__ == "__main__":
    host = "127.0.0.1" 
    port = 24596

    client = SCPIClient(host, port)

    # Example SCPI queries
    print("Querying instrument identity")
    print(f'Response: client.query("*IDN?")')

    print("Querying available options")
    print(f'Response: client.query("*OPT?")')

    print("Querying measurement reading")
    print(f'Response: client.query("READ?")')

    print("Querying voltage setting")
    print(f'Response: client.query("VOLTage?")')

    print("Querying frequency setting")
    print(f'Response: client.query("FREQ?")')

