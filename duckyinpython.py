# License : GPLv2.0
# copyright (c) 2021  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)


import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse

# mouse jiggler configuration
mouseJigglerDelayMin = 1
mouseJigglerDelayMax = 15
mouseJigglerMovement = 10
mouseJigglerLED = True

# comment out these lines for non_US keyboards
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode

# uncomment these lines for non_US keyboards
# replace LANG with appropriate language
#from keyboard_layout_win_LANG import KeyboardLayout
#from keycode_win_LANG import Keycode

import time
import digitalio
import random
from board import *
led = digitalio.DigitalInOut(LED)
led.direction = digitalio.Direction.OUTPUT

duckyCommands = {
    'WINDOWS': Keycode.WINDOWS, 'GUI': Keycode.GUI,
    'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION, 'SHIFT': Keycode.SHIFT,
    'ALT': Keycode.ALT, 'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL,
    'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
    'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
    'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
    'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
    'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
    'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
    'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
    'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
    'BACKSPACE': Keycode.BACKSPACE,
    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
    'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
    'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
    'F12': Keycode.F12,
}

mouseCommands = {
    'LEFT': Mouse.LEFT_BUTTON, 'RIGHT': Mouse.RIGHT_BUTTON, 'MIDDLE': Mouse.MIDDLE_BUTTON
}

def pickInterval():
    return time.monotonic(), (random.randint(mouseJigglerDelayMin, mouseJigglerDelayMax))

def blinkLED(duration, repeats=1):
    if mouseJigglerLED:
        for i in range(repeats):
            led.value = True
            time.sleep(duration)
            led.value = False
            time.sleep(duration)

def mouseJigglerLoop():
    # blink LED 6x (startup indicator)
    blinkLED(0.08, 6)

    print("Running mouse jiggler")
    print(" > movement  =", mouseJigglerMovement, "px")
    print(" > delay min =", mouseJigglerDelayMin, "second(s)")
    print(" > delay max =", mouseJigglerDelayMax, "seconds")

    timestamp, interval = pickInterval()

    print("waiting", interval, "seconds")
    while True:
        if (time.monotonic() - timestamp) > interval:
            # move mouse up+left then back down+right
            print("jiggling mouse", mouseJigglerMovement, "pixels")
            mouse.move(x=-mouseJigglerMovement, y=-mouseJigglerMovement)
            mouse.move(x=mouseJigglerMovement, y=mouseJigglerMovement)

            # blink LED
            blinkLED(0.15)

            # determine delay
            timestamp, interval = pickInterval()
            print("waiting", interval, "seconds")

def loadLocale(locale):
    global KeyboardLayout, Keycode, layout
    if(locale.lower() == "us"):
        moduleKeyboardLayout = __import__("adafruit_hid.keyboard_layout_us", globals(), locals(), ["KeyboardLayoutUS"])
        moduleKeycode = __import__("adafruit_hid.keycode", globals(), locals(), ["Keycode"])
        KeyboardLayout = moduleKeyboardLayout.KeyboardLayoutUS
        Keycode = moduleKeycode.Keycode
    else:
        moduleKeyboardLayout = __import__("keyboard_layout_win_" + locale.lower(), globals(), locals(), ["KeyboardLayout"])
        moduleKeycode = __import__("keycode_win_" + locale.lower(), globals(), locals(), ["Keycode"])
        KeyboardLayout = moduleKeyboardLayout.KeyboardLayout
        Keycode = moduleKeycode.Keycode
    layout = KeyboardLayout(kbd)

def convertLine(line):
    newline = []
    print(line)
    # loop on each key - the filter removes empty values
    for key in filter(None, line.split(" ")):
        key = key.upper()
        # find the keycode for the command in the list
        command_keycode = duckyCommands.get(key, None)
        if command_keycode is not None:
            # if it exists in the list, use it
            newline.append(command_keycode)
        elif hasattr(Keycode, key):
            # if it's in the Keycode module, use it (allows any valid keycode)
            newline.append(getattr(Keycode, key))
        else:
            # if it's not a known key name, show the error for diagnosis
            print(f"Unknown key: <{key}>")
    print(newline)
    return newline

def runScriptLine(line):
    for k in line:
        kbd.press(k)
    kbd.release_all()

def sendString(line):
    layout.write(line)

def getMouseButtons(line):
    buttons = line.split(" ")
    command = 0
    for button in buttons:
        command |= mouseCommands.get(button, None)
    return command

def mouseAction(line):
    if(line[0:4] == "MOVE"):
        coordinates = line[5:].split(" ")
        moveX = int(coordinates[0])
        moveY = int(coordinates[1])
        mouse.move(x=moveX, y=moveY)
    elif(line[0:5] == "WHEEL"):
        amount = int(line[6:])
        mouse.move(wheel=amount)
    elif(line[0:5] == "CLICK"):
        mouse.click(getMouseButtons(line[6:]))
    elif(line[0:5] == "PRESS"):
        mouse.press(getMouseButtons(line[6:]))
    elif(line[0:7] == "RELEASE"):
        mouse.release(getMouseButtons(line[8:]))
    elif(line[0:10] == "RELEASEALL"):
        mouse.release_all()

def parseLine(line):
    global defaultDelay
    if(line[0:3] == "REM"):
        # ignore ducky script comments
        pass
    elif(line[0:5] == "DELAY"):
        time.sleep(float(line[6:])/1000)
    elif(line[0:6] == "STRING"):
        sendString(line[7:])
    elif(line[0:5] == "PRINT"):
        print("[SCRIPT]: " + line[6:])
    elif(line[0:13] == "DEFAULT_DELAY"):
        defaultDelay = int(line[14:]) * 10
    elif(line[0:12] == "DEFAULTDELAY"):
        defaultDelay = int(line[13:]) * 10
    elif(line[0:3] == "LED"):
        led.value = not led.value
    elif(line[0:6] == "IMPORT"):
        processDuckyScript(line[7:])
    elif(line[0:6] == "LOCALE"):
        loadLocale(line[7:])
    elif(line[0:5] == "MOUSE"):
        mouseAction(line[6:])
    else:
        newScriptLine = convertLine(line)
        runScriptLine(newScriptLine)

def processDuckyScript(duckyScriptPath):
    f = open(duckyScriptPath, "r", encoding='utf-8')
    print("Running " + duckyScriptPath)
    previousLine = ""
    duckyScript = f.readlines()
    for line in duckyScript:
        line = line.rstrip()
        if(line[0:6] == "REPEAT"):
            for i in range(int(line[7:])):
                # repeat the last command
                parseLine(previousLine)
                time.sleep(float(defaultDelay)/1000)
        else:
            parseLine(line)
            previousLine = line
        time.sleep(float(defaultDelay)/1000)
    print("Done")

def isPinGrounded(pin):
    checkPin = digitalio.DigitalInOut(pin)
    checkPin.switch_to_input(pull=digitalio.Pull.UP)
    return (not checkPin.value)

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
layout = KeyboardLayout(kbd)

# sleep at the start to allow the device to be recognized by the host computer
time.sleep(.5)

defaultDelay = 0

# check GP0/GP1/GP2/GP3/GP4/GP5/GP6 for run mode
if isPinGrounded(GP0):
    processDuckyScript("payload0.dd")
elif isPinGrounded(GP1):
    processDuckyScript("payload1.dd")
elif isPinGrounded(GP2):
    processDuckyScript("payload2.dd")
elif isPinGrounded(GP3):
    processDuckyScript("payload3.dd")
elif isPinGrounded(GP4):
    processDuckyScript("payload4.dd")
elif isPinGrounded(GP5):
    processDuckyScript("payload5.dd")
elif isPinGrounded(GP6):
    mouseJigglerLoop()
else:
    # in setup mode
    print("Update your payload")
