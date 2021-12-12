import pyautogui
import sys
import cv2
import numpy as np
from PIL import ImageGrab

import os, re, sys, time
from subprocess import PIPE, Popen

def print_cursor_position():
    print("Press Ctr-C to quit.")
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')


def grab_screen(region=None):
    screen_w = 1920
    screen_h = 1080

    if region:
        left,top,x2,y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = screen_w
        height = screen_h
        left = 0
        top = 0

    rgb = ImageGrab.grab(bbox=(left, top, width, height))
    # rgb = ImageGrab.grab()
    rgb = np.array(rgb)

    return cv2.cvtColor(rgb, cv2.COLOR_BGRA2BGR)


def get_activityname():

    root = Popen( ['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout = PIPE )
    stdout, stderr = root.communicate()
    m = re.search( b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout )

    if m is not None:

        window_id   = m.group( 1 )

        windowname  = None
        window = Popen( ['xprop', '-id', window_id, 'WM_NAME'], stdout = PIPE )
        stdout, stderr = window.communicate()
        wmatch = re.match( b'WM_NAME\(\w+\) = (?P<name>.+)$', stdout )
        if wmatch is not None:
            windowname = wmatch.group( 'name' ).decode( 'UTF-8' ).strip( '"' )

        processname1, processname2 = None, None
        process = Popen( ['xprop', '-id', window_id, 'WM_CLASS'], stdout = PIPE )
        stdout, stderr = process.communicate()
        pmatch = re.match( b'WM_CLASS\(\w+\) = (?P<name>.+)$', stdout )
        if pmatch is not None:
            processname1, processname2 = pmatch.group( 'name' ).decode( 'UTF-8' ).split( ', ' )
            processname1 = processname1.strip( '"' )
            processname2 = processname2.strip( '"' )

        return {
            'windowname':   windowname,
            'processname1': processname1,
            'processname2': processname2
            }

    return {
        'windowname':   None,
        'processname1': None,
        'processname2': None
        }


if __name__ == '__main__':
    a = get_activityname()
    print( '''
    'windowname':   %s,
    'processname1': %s,
    'processname2': %s
    ''' % ( a['windowname'], a['processname1'], a['processname2'] ) )
