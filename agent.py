import logging
import numpy as np
import neat

from keys import *


KEY_BINDS = {
    "Nothing": 'nothing',
    "Jump": 'space',
    "Sneak": 'shiftleft',
    "Sprint": "ctrlleft",
    "Strafe Left": 'a',
    "Strafe Right": 's',
    "Walk Backwards": 's',
    "Walk Forwards": 'w',
    "Attack": 'lmousebutton',
    "Pick Block": 'mmousebutton',
    "Use Item/Place Block": 'rmousebutton',
    "Drop Selected Item": 'q',
    "Open/Close Inventory": 'e',
    "Swap Item With Offhand": 'f',
    "Slot 1": '1',
    "Slot 2": '2',
    "Slot 3": '3',
    "Slot 4": '4',
    "Slot 5": '5',
    "Slot 6": '6',
    "Slot 7": '7',
    "Slot 8": '8',
    "Slot 9": '9'
}

MOVES = {
    -1: "Nothing",
    0: "Jump",
    1: "Sneak",
    2: "Sprint",
    3: "Strafe Left",
    4: "Strafe Right",
    5: "Walk Backwards",
    6: "Walk Forwards",
    7: "Attack",
    8: "Pick Block",
    9: "Use Item/Place Block",
    10: "Drop Selected Item",
    11: "Open/Close Inventory",
    12: "Swap Item With Offhand",
    13: "Slot 1",
    14: "Slot 2",
    15: "Slot 3",
    16: "Slot 4",
    17: "Slot 5",
    18: "Slot 6",
    19: "Slot 7",
    20: "Slot 8",
    21: "Slot 9",



}

MOVE_TIME = 0.2


class NeatAgent:
    def __init__(self, genome, config):
        super(NeatAgent, self).__init__()

        self.genome = genome
        self.config = config

        self.net = neat.nn.FeedForwardNetwork.create(genome, config)

    def act(self, observation, step=None):
        action = np.argmax(self.net.activate(observation))



class Agent:
    def __init__(self):
        super(Agent, self).__init__()
        # self.keys = Keys()

        self.model = None

        self.moves = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def act(self, observation, step=None):
        """
        Given a state choose a random action from action space(For now)
        We'll update functionality later
        """

        if observation is not None:
            if step == 0:
                self.do_move(MOVES[-1])
            else:
                move = np.random.choice(self.moves, size=1)
                # move = self.model(observation)
                self.do_move(MOVES[move[0]])

    def do_move(self, move):

        if KEY_BINDS[move] == 'lmousebutton':
            pyautogui.mouseDown()
            sleep(MOVE_TIME)
            pyautogui.mouseUp()
            # pyautogui.click()
        elif KEY_BINDS[move] == 'mmousebutton':
            pyautogui.mouseDown(button='middle')
            sleep(MOVE_TIME)
            pyautogui.mouseUp(button='middle')
            # pyautogui.click()
        elif KEY_BINDS[move] == 'rmousebutton':
            pyautogui.mouseDown(button='right')
            sleep(MOVE_TIME)
            pyautogui.mouseUp(button='right')
        elif KEY_BINDS[move] == 'nothing':
            print("Nothing to do!")
            # logging.info(f"Nothing to do!!")
            # pyautogui.click(button='right')
        else:
            pyautogui.keyDown(KEY_BINDS[move])
            sleep(MOVE_TIME)
            pyautogui.keyUp(KEY_BINDS[move])

        # if move == "jump":
        #     # self.keys.direct_key("SPACE")
        #     pyautogui.keyDown('space')
        #     sleep(MOVE_TIME)
        #     pyautogui.keyUp('space')
        #     # self.keys.direct_key("SPACE")
        # elif move == "forward":
        #     pyautogui.keyDown('w')
        #     sleep(MOVE_TIME)
        #     pyautogui.keyUp('w')
        #     # self.keys.direct_key("W")
        # elif move == "backwards":
        #     self.keys.direct_key("S")
        #     pyautogui.keyDown('s')
        #     sleep(MOVE_TIME)
        #     pyautogui.keyUp('s')
        #     # self.keys.direct_key("S")
        # elif move == "left":
        #     # self.keys.direct_key("A")
        #     pyautogui.keyDown('a')
        #     sleep(MOVE_TIME)
        #     pyautogui.keyUp('a')
        #     # self.keys.direct_key("A")
        # elif move == "right":
        #     # self.keys.direct_key("D")
        #     pyautogui.keyDown('d')
        #     sleep(MOVE_TIME)
        #     pyautogui.keyUp('d')
        #     # self.keys.direct_key("D")

    def do_random_action(self):
        # mouse movement
        for i in range(100):
            self.keys.direct_mouse(-1*i, 0)
            sleep(0.004)
            break

    def learn(self, observation, actions):
        if observation is not None:
            raise "Not Implemented error"
        else:
            pass


