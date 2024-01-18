#! /usr/bin/env python

import signal
import socket
import re


class SCPICommand:
    def __init__(self, command, value, read_only=False):
        self.command = command
        
        abbrev_pattern = re.compile(r'^([A-Z]+)([A-Za-z]*)')
        parsed = abbrev_pattern.search(self.command)
        if parsed == None:
            raise RuntimeError(f'Invalid SCPI command: {command}')
        self.short = parsed.group(1).casefold()
        self.long = (parsed.group(1) + parsed.group(2)).casefold()

        self.value = value
        self.read_only = read_only

    def handle(self, command_tokens):
        if not self.compare(command_tokens[0]):
            return False, None
        
        if command_tokens[0][-1] == '?':
            return self.get()
        
        if self.read_only:
            raise RuntimeError(f'Command {self.command} is read-only')
        
        return self.set(command_tokens)

    def compare(self, command):
        command = command.lstrip('*').rstrip('?').casefold()
        return True if command == self.short or command == self.long else False
    
    def get(self):
        return True, self.value
    
    def set(self, command_tokens):
        self.value = command_tokens[1:]
        return True, None

class ASCPIDevice:
    """
    This class represents a SCPI-compliant device.

    Note that you won't use a class like this in an actual Dripline deployment --- 
    this takes the place of an actual device for the purpose of this tutorial.

    This class was composed with the aid of ChatGPT 3.5.
    """
    def __init__(self, host, port, commands, ending='\n'):
        self.host = host
        self.port = port
        self.socket = None

        self.ending = ending

        self.commands = [ SCPICommand(key, value) for (key, value) in commands ]

        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        self.disconnect()
    
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            self.socket.bind((self.host, self.port))
            while self.socket.fileno() > 0:
                print(f"Listening for connections on {self.host}:{self.port}")
                self.socket.listen(1)
                try:
                    self.connection, addr = self.socket.accept()
                except:
                    break
                print(f'Connected to client from {addr}')
                self.receive_data()

    def disconnect(self):
        if self.socket:
            self.socket.close()
        print("Disconnected")

    def handle_query(self, query):
        tokens = query.split()
        try:
            for command in self.commands:
                success, response = command.handle(tokens)
                if success:
                    return str(response)
            return "Invalid request"
        except RuntimeError as e:
            return str(e)

    def receive_data(self):
        data = ''
        while True:
            try:
                print('Receiving data')
                data += self.connection.recv(1024).decode('utf-8')
                if data.endswith(self.ending):
                    break
                print('Adding data')
                print(f'So far: {repr(data)}')
            except Exception as e:
                print(f"Error: {e}")
                break

        print(f'Received query: {repr(data)}')
        if data:
            response = str(self.handle_query(data)) + self.ending
            print(f'Sending response <{repr(response)}>')
            self.connection.send(response.encode('utf-8'))


if __name__ == "__main__":
    host = "127.0.0.1" 
    port = 24596

    commands = {
        'IDN': 'Instrument Model XYZ,1234,1.0,Serial123456',
        'OPT': 'Option1,Option2,Option3',
        'READ': 42.0,
        'VOLTage': 3.14,
        'FREQuency': 1.05457,
    }

    scpi_handler = ASCPIDevice(host, port)
    scpi_handler.start()
