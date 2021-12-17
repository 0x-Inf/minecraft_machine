import logging
from time import time, sleep

import numpy as np
import pyautogui
import cv2
import argparse
# import pygetwindow as gw

from grabscreen import grab_screen
from agent import Agent

parser = argparse.ArgumentParser()
parser.add_argument("--agent_preset", help="type of agent you want to play the game")
parser.add_argument("--view_obs", help="yes if you want to see what agent is seeing")

logging.basicConfig(filename="main.log", level=logging.INFO)


def do_random_stuff():
    for i in range(10):  # Move mouse in a square.
        pyautogui.moveTo(100, 100, duration=0.25)
        pyautogui.moveTo(200, 100, duration=0.25)
        pyautogui.moveTo(200, 200, duration=0.25)
        pyautogui.moveTo(100, 200, duration=0.25)

    for i in range(10):  # Move mouse in square relative to starting position
        pyautogui.move(100, 0, duration=0.25)  # right
        pyautogui.move(0, 100, duration=0.25)  # down
        pyautogui.move(-100, 0, duration=0.25)  # left
        pyautogui.move(0, -100, duration=0.25)  # up

    mouse_position = pyautogui.position()

    # mouse clicks
    pyautogui.click(button='right')
    sleep(0.5)
    pyautogui.click()
    sleep(2)
    pyautogui.click()
    sleep(0.5)
    pyautogui.click(button='right')
    # Move mouse to (10, 5) and click.
    pyautogui.click(10, 5)

    # Mouse up and down

    # # keyboard (direct keys)
    # keys.directKey("a")
    # sleep(0.04)
    # keys.directKey("a", keys.key_release)
    #
    # # keyboard (virtual keys)
    # keys.directKey("a", type=keys.virtual_keys)
    # sleep(0.04)
    # keys.directKey("a", keys.key_release, keys.virtual_keys)
    #
    # # queue of keys (direct keys, threaded, only for keybord input)
    # keys.parseKeyString("a_down,-4,a_up,0x01")  # -4 - pause for 4 ms, 0x00 - hex code of Esc
    #
    # # queue of keys (virtual keys, threaded, only for keybord input)
    # keys.parseKeyString("vk,a_down,-4,a_up")  # -4 - pause for 4 ms


def find_position_of_image(img):
    raise "Not Implemted Error"


def move_window_highlight_craft():
    pyautogui.moveTo(461, 157)
    sleep(0.5)
    pyautogui.dragTo(171, 593, button='left')
    sleep(0.5)
    pyautogui.click(x=114, y=4)
    sleep(0.5)
    pyautogui.moveTo(481, 221)
    sleep(0.5)
    pyautogui.click()
    sleep(0.5)
    print(f"Mine should be crafting!")


def highlight_craft():
    pyautogui.moveTo(477, 50)
    sleep(0.5)
    pyautogui.click()
    sleep(0.5)
    pyautogui.moveTo(481, 221)
    sleep(0.5)
    pyautogui.click()
    sleep(0.5)
    print(f"Mine should be crafting!")


def get_observation(screen):
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    observation = screen_gray
    return observation


def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        sleep(1)

    last_time = time()
    total_time = 0
    observation_step = 0

    agent = Agent()
    args = parser.parse_args()

    while True:
        screen = grab_screen(region=(60, 64, 970, 605))
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        observation = get_observation(screen)

        if args.view_obs == "yes":
            if observation_step == 1:
                move_window_highlight_craft()
        else:
            if observation_step == 1:
                highlight_craft()

        if args.agent_preset == "dead":
            agent.learn(None, None)
        elif args.agent_preset == "alive":
            logging.info(f"Passing observation: {observation_step} to agent")
            agent.act(observation, step=observation_step)
            # sleep(2)

        output_img = screen_gray

        loop_time = time() - last_time
        logging.info(f'loop took {loop_time} seconds')
        print(f"Observation Step: {observation_step}")
        total_time += loop_time
        last_time = time()
        observation_step += 1
        if int(total_time) == 10:
            logging.info(f'Total Time: {total_time}')
            logging.info(f"Observation Step: {observation_step}")

        if args.view_obs == "yes":
            cv2.imshow('window', output_img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        else:
            pass


if __name__ == '__main__':
    main()
