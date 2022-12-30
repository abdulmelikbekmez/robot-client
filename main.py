from socket import socket, AF_INET, SOCK_STREAM
import sys
import json
from pynput import keyboard

class App:
    def __init__(self) -> None:
        self.ip = "172.20.19.43"
        self.port = 5000
        self.socket = None

    def __del__(self):
        self.socket = None
    
    def send(self, jsonn:dict):
        if not self.socket:
            return
        req = json.dumps(jsonn)
        self.socket.sendall(bytes(req, encoding="utf-8"))
        print(f"sended data => {req}")

    def get_action(self, char:str):
        if char == 'w':
            return 0
        if char == 's':
            return 1

        if char == 'a':
            return 2

        if char == 'd':
            return 3

        return 4

    def on_press(self, key):

        if key == keyboard.Key.esc:
            print("esc pressed")
            return False  # stop listener
        k=None
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
            # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        self.send({"Action": self.get_action(k)})
        # return False  # stop listener; remove this if want more keys
    
    def start(self):
        req = {"Introduce": 0}

        with socket(AF_INET, SOCK_STREAM) as s:
            try:
                s.connect((self.ip, self.port))
            except ConnectionError as e:
                print(e)
                print("Aborting the program...")
                sys.exit()
            self.socket = s
            self.send(req)

            listener = keyboard.Listener(on_press=self.on_press)
            listener.start()  # start to listen on a separate thread
            listener.join()  # remove if main thread is polling self.keys

App().start()
