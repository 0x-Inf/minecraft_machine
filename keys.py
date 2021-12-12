import ctypes
from threading import Thread
from time import time, sleep
from queue import Queue
import pyautogui

PYAUTOGUI_KEYS = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
                  ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
                  '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                  'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
                  'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
                  'browserback', 'browserfavorites', 'browserforward', 'browserhome',
                  'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
                  'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
                  'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                  'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                  'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                  'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
                  'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                  'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                  'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                  'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                  'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                  'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                  'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                  'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                  'command', 'option', 'optionleft', 'optionright']


# main Key class
class Keys:
    common = None
    standalone = False

    # Instance of worker class
    keys_worker = None
    key_process = None

    # key constants
    direct_keys = 0x0008
    virtual_keys = 0x0000
    key_press = 0x0000
    key_release = 0x0002

    # Mouse constants
    mouse_move = 0x0001
    mouse_lb_press = 0x0002
    mouse_lb_release = 0x0004
    mouse_rb_press = 0x0008
    mouse_rb_release = 0x0010
    mouse_mb_press = 0x0020
    mouse_mb_release = 0x0040

    # direct keys
    dk = {
        "1": '1',
        "2": '2',
        "3": '3',
        "4": '4',
        "5": '5',
        "6": '6',
        "7": '7',
        "8": '8',
        "9": '9',
        "0": '0',

        "NUMPAD1": 'num1', "NP1": 'num1',
        "NUMPAD2": 'num2', "NP2": '2',
        "NUMPAD3": 'num3', "NP3": '3',
        "NUMPAD4": 'num4', "NP4": '4',
        "NUMPAD5": 'num5', "NP5": 'num5',
        "NUMPAD6": 'num6', "NP6": 'num6',
        "NUMPAD7": 'num7', "NP7": 'num7',
        "NUMPAD8": 'num8', "NP8": 'num8',
        "NUMPAD9": 'num9', "NP9": 'num9',
        "NUMPAD0": 'num0', "NP0": 'num0',
        "DIVIDE": 'divide', "NPDV": 'divide',
        "MULTIPLY": 'multiply', "NPM": 'multiply',
        "SUBSTRACT": 'subtract', "NPS": 'subtract',
        "ADD": 'add', "NPA": 'add',
        "DECIMAL": 'decimal', "NPDC": 'decimal',
        "NUMPADENTER": 'enter', "NPE": 'enter',

        "A": 'a',
        "B": 'b',
        "C": 'c',
        "D": 'd',
        "E": 'e',
        "F": 'f',
        "G": 'g',
        "H": 'h',
        "I": 'i',
        "J": 'j',
        "K": 'k',
        "L": 'l',
        "M": 'm',
        "N": 'n',
        "O": 'o',
        "P": 'p',
        "Q": 'q',
        "R": 'r',
        "S": 's',
        "T": 't',
        "U": 'u',
        "V": 'v',
        "W": 'w',
        "X": 'x',
        "Y": 'y',
        "Z": 'z',

        "F1": 'f1',
        "F2": 'f2',
        "F3": 'f3',
        "F4": 'f4',
        "F5": 'f5',
        "F6": 'f6',
        "F7": 'f7',
        "F8": 'f8',
        "F9": 'f9',
        "F10": 'f10',
        "F11": 'f11',
        "F12": 'f12',

        "UP": 'up',
        "LEFT": 'left',
        "RIGHT": 'right',
        "DOWN": 'down',

        "ESC": 'esc',
        "SPACE": 'space', "SPC": 'space',
        "RETURN": 'enter', "ENT": 'enter',
        "INSERT": 'insert', "INS": 'insert',
        "DELETE": 'delete', "DEL": 'delete',
        "HOME": 'home',
        "END": 'end',
        "PRIOR": '', "PGUP": 'pgup',
        "NEXT": '', "PGDN": 'pgdn',
        "BACK": 'backspace',
        "TAB": 'tab',
        "LCONTROL": 'ctrlleft', "LCTRL": 'ctrlleft',
        "RCONTROL": 'ctrlright', "RCTRL": 'ctrlright',
        "LSHIFT": 'shiftleft', "LSH": 'shiftleft',
        "RSHIFT": 'shiftright', "RSH": 'shiftright',
        "LMENU": '', "LALT": 'altleft',
        "RMENU": '', "RALT": 'altright',
        "LWIN": '',
        "RWIN": '',
        "APPS": 'apps',
        "CAPITAL": 'capslock', "CAPS": 'capslock',
        "NUMLOCK": 'numlock', "NUM": 'numlock',
        "SCROLL": 'scrolllock', "SCR": 'scrolllock',

        "MINUS": '-', "MIN": '-',
        "LBRACKET": '(', "LBR": '(',
        "RBRACKET": ')', "RBR": ')',
        "SEMICOLON": ';', "SEM": ';',
        "APOSTROPHE": '', "APO": '',
        "GRAVE": '', "GRA": '',
        "BACKSLASH": '/', "BSL": '/',
        "COMMA": ',', "COM": ',',
        "PERIOD": '.', "PER": '.',
        "SLASH": '/', "SLA": '/',

    }

    # virtual keys
    vk = {
        "1": '1',
        "2": '2',
        "3": '3',
        "4": '4',
        "5": '5',
        "6": '6',
        "7": '7',
        "8": '8',
        "9": '9',
        "0": '0',

        "NUMPAD1": 'num1', "NP1": 'num1',
        "NUMPAD2": 'num2', "NP2": '2',
        "NUMPAD3": 'num3', "NP3": '3',
        "NUMPAD4": 'num4', "NP4": '4',
        "NUMPAD5": 'num5', "NP5": 'num5',
        "NUMPAD6": 'num6', "NP6": 'num6',
        "NUMPAD7": 'num7', "NP7": 'num7',
        "NUMPAD8": 'num8', "NP8": 'num8',
        "NUMPAD9": 'num9', "NP9": 'num9',
        "NUMPAD0": 'num0', "NP0": 'num0',
        "DIVIDE": 'divide', "NPDV": 'divide',
        "MULTIPLY": 'multiply', "NPM": 'multiply',
        "SUBSTRACT": 'subtract', "NPS": 'subtract',
        "ADD": 'add', "NPA": 'add',
        "DECIMAL": 'decimal', "NPDC": 'decimal',
        "NUMPADENTER": 'enter', "NPE": 'enter',

        "A": 'a',
        "B": 'b',
        "C": 'c',
        "D": 'd',
        "E": 'e',
        "F": 'f',
        "G": 'g',
        "H": 'h',
        "I": 'i',
        "J": 'j',
        "K": 'k',
        "L": 'l',
        "M": 'm',
        "N": 'n',
        "O": 'o',
        "P": 'p',
        "Q": 'q',
        "R": 'r',
        "S": 's',
        "T": 't',
        "U": 'u',
        "V": 'v',
        "W": 'w',
        "X": 'x',
        "Y": 'y',
        "Z": 'z',

        "F1": 'f1',
        "F2": 'f2',
        "F3": 'f3',
        "F4": 'f4',
        "F5": 'f5',
        "F6": 'f6',
        "F7": 'f7',
        "F8": 'f8',
        "F9": 'f9',
        "F10": 'f10',
        "F11": 'f11',
        "F12": 'f12',

        "UP": 'up',
        "LEFT": 'left',
        "RIGHT": 'right',
        "DOWN": 'down',

        "ESC": 'esc',
        "SPACE": 'space', "SPC": 'space',
        "RETURN": 'enter', "ENT": 'enter',
        "INSERT": 'insert', "INS": 'insert',
        "DELETE": 'delete', "DEL": 'delete',
        "HOME": 'home',
        "END": 'end',
        "PRIOR": '', "PGUP": 'pgup',
        "NEXT": '', "PGDN": 'pgdn',
        "BACK": 'backspace',
        "TAB": 'tab',
        "LCONTROL": 'ctrlleft', "LCTRL": 'ctrlleft',
        "RCONTROL": 'ctrlright', "RCTRL": 'ctrlright',
        "LSHIFT": 'shiftleft', "LSH": 'shiftleft',
        "RSHIFT": 'shiftright', "RSH": 'shiftright',
        "LMENU": '', "LALT": 'altleft',
        "RMENU": '', "RALT": 'altright',
        "LWIN": '',
        "RWIN": '',
        "APPS": 'apps',
        "CAPITAL": 'capslock', "CAPS": 'capslock',
        "NUMLOCK": 'numlock', "NUM": 'numlock',
        "SCROLL": 'scrolllock', "SCR": 'scrolllock',

        "MINUS": '-', "MIN": '-',
        "LBRACKET": '(', "LBR": '(',
        "RBRACKET": ')', "RBR": ')',
        "SEMICOLON": ';', "SEM": ';',
        "APOSTROPHE": '', "APO": '',
        "GRAVE": '', "GRA": '',
        "BACKSLASH": '/', "BSL": '/',
        "COMMA": ',', "COM": ',',
        "PERIOD": '.', "PER": '.',
        "SLASH": '/', "SLA": '/',

    }

    # Setup Object
    def __init__(self, common=None):
        self.keys_worker = KeysWorker(self)
        self.common = common
        if common is None:
            self.standalone = True

    # Parse keys strings and add key to the queue
    def parse_key_string(self, string):

        # print keys
        if not self.standalone:
            self.common.info("Processing key: %s" % string)

        key_queue = []
        errors = []

        # Default to direct keys
        key_type = self.direct_keys

        # Split by comma
        keys = string.upper().split(",")

        # translate
        for key in keys:

            # Up, Down or stroke?
            up = True
            down = True
            direction = key.split("_")
            subkey = direction[0]
            if len(direction) >= 2:
                if direction[1] == 'UP':
                    down = False
                else:
                    up = False

            # switch to virtual keys
            if subkey == "VK":
                key_type = self.virtual_keys

            # switch to Direct keys
            if subkey == "DK":
                key_type = self.direct_keys

            # key code
            elif subkey.startswith("0x"):
                subkey = int(subkey, 16)
                if subkey > 0 and subkey < 256:
                    key_queue.append({
                        "key": int(subkey),
                        "okey": subkey,
                        "time": 0,
                        "up": up,
                        "down": down,
                        "type": key_type
                    })
                else:
                    errors.append(key)

            # pause
            elif subkey.startswith("-"):
                time = float(subkey.replace("-", "")) / 1000
                if time > 0 and time <= 10:
                    key_queue.append({
                        "key": None,
                        "okey": "",
                        "time": time,
                        "up": False,
                        "down": False,
                        "type": None,
                    })
                else:
                    errors.append(key)

            # direct key
            elif key_type == self.direct_keys and subkey in self.dk:
                key_queue.append({
                    "key": self.dk[subkey],
                    "okey": subkey,
                    "time": 0,
                    "up": up,
                    "down": down,
                    "type": key_type,
                })

            # virtual key
            elif key_type == self.virtual_keys and subkey in self.vk:
                key_queue.append({
                    "key": self.vk[subkey],
                    "okey": subkey,
                    "time": 0,
                    "up": up,
                    "down": down,
                    "type": key_type,
                })

            # no match?
            else:
                errors.append(key)

        # If there are errors do not process keys
        if len(errors):
            return errors

        # Create a new thread if there is no active one
        if self.key_process is None or not self.key_process.isAlive():
            self.key_process = Thread(target=self.keys_worker.processQueue())
            self.key_process.start()

        # Add keys to queue
        for i in key_queue:
            self.keys_worker.key_queue.put(i)
        self.keys_worker.key_queue.put(None)

        return True

    # Direct key press
    def direct_key(self, key, direction=None, type=None):
        if type is None:
            type = self.direct_keys
        if direction is None:
            direction = self.key_press

        key = key.upper()
        lookup_table = self.dk if type == self.direct_keys else self.vk
        key = lookup_table[key] if key in lookup_table else "nokey"

        self.keys_worker.sendKey(key)

    # Direct Mouse move or button press
    def direct_mouse(self, dx=0, dy=0, buttons=0):
        self.keys_worker.sendMouse(dx, dy, buttons)


# threaded sending keys class
class KeysWorker:
    # keys object
    keys = None

    # queue of keys
    key_queue = Queue()

    # init
    def __init__(self, keys):
        self.keys = keys

    # main function, process key's quue in loop
    def processQueue(self):

        # endless loop
        while True:

            # get one key
            key = self.key_queue.get()

            # terminate process if queue is empty
            if key is None:
                self.key_queue.task_done()
                if self.key_queue.empty():
                    return
                continue

            # Print key
            elif not self.keys.standalone:
                self.keys.common.info(
                    "Key: \033[1;35m%s/%s\033[0;37m, duration: \033[1;35m%f\033[0;37m, direction: \033[1;35m%s\033[0;37m, type: \033[1;35m%s" % (
                        key["okey"] if key["okey"] else "None",
                        key["key"], key["time"],
                        "UP" if key["up"] and not key["down"] else "DOWN" if not key["up"] and key[
                            "down"] else "BOTH" if key["up"] and key["down"] else "None",
                        "None" if key["type"] is None else "DK" if key["type"] == self.keys.direct_keys else "VK"),
                    "\033[0;35mKEY:   \033[0;37m"
                    )

            # if it's a key
            if key["key"]:

                # press
                if key["down"]:
                    self.sendKey(key["key"], self.keys.key_press | key["type"])

                # wait
                sleep(key["time"])

                # and release
                if key["up"]:
                    self.sendKey(key["key"], self.keys.key_release | key["type"])


            # not an actual key, just pause
            else:
                sleep(key["time"])

            # mark as done (decrement internal queue counter)
            self.key_queue.task_done()

    # send key
    def sendKey(self, key):
        self.Keyboard(key)

    # send mouse
    def sendMouse(self, dx, dy, buttons):
        if dx != 0 or dy != 0:
            buttons |= self.keys.mouse_move
        self.Mouse(buttons, dx, dy)

    # mouse input
    def MouseInput(self, flags, x, y, data):
        return pyautogui.moveTo(x, y)

    # keyboard input
    def KeybdInput(self, code):
        print(f"The key code {code.lower()}")
        return pyautogui.press(code)


    # mouse object
    def Mouse(self, flags, x=0, y=0, data=0):
        return self.MouseInput(flags, x, y, data)

    # keyboard object
    def Keyboard(self, code):
        self.KeybdInput(code)
