# License : GPLv2.0
# copyright (c) 2021  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)

import random
import time

import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from board import *
from digitalio import DigitalInOut, Direction, Pull

# import configuration
try:
    from pd.config import config
except ImportError:
    print(
        "Using default configuration (config_default.py). To use your own settings copy as config.py and modify to taste."
    )
    from pd.config_default import config


# map duckyscript commands to keycodes
duckyCommands = {
    "ALT": Keycode.ALT,
    "APP": Keycode.APPLICATION,
    "BACKSPACE": Keycode.BACKSPACE,
    "BREAK": Keycode.PAUSE,
    "CAPSLOCK": Keycode.CAPS_LOCK,
    "COMMAND": Keycode.COMMAND,
    "CONTROL": Keycode.CONTROL,
    "CTRL": Keycode.CONTROL,
    "DELETE": Keycode.DELETE,
    "END": Keycode.END,
    "ENTER": Keycode.ENTER,
    "ESC": Keycode.ESCAPE,
    "ESCAPE": Keycode.ESCAPE,
    "GUI": Keycode.GUI,
    "HOME": Keycode.HOME,
    "INSERT": Keycode.INSERT,
    "MENU": Keycode.APPLICATION,
    "NUMLOCK": Keycode.KEYPAD_NUMLOCK,
    "OPTION": Keycode.OPTION,
    "PAGEDOWN": Keycode.PAGE_DOWN,
    "PAGEUP": Keycode.PAGE_UP,
    "PAUSE": Keycode.PAUSE,
    "POWER": Keycode.POWER,
    "PRINTSCREEN": Keycode.PRINT_SCREEN,
    "RIGHTALT": Keycode.RIGHT_ALT,
    "RIGHTCONTROL": Keycode.RIGHT_CONTROL,
    "RIGHTGUI": Keycode.RIGHT_GUI,
    "RIGHTSHIFT": Keycode.RIGHT_SHIFT,
    "SCROLLLOCK": Keycode.SCROLL_LOCK,
    "SHIFT": Keycode.SHIFT,
    "SPACE": Keycode.SPACE,
    "TAB": Keycode.TAB,
    "WINDOWS": Keycode.WINDOWS,
    "A": Keycode.A,
    "B": Keycode.B,
    "C": Keycode.C,
    "D": Keycode.D,
    "E": Keycode.E,
    "F": Keycode.F,
    "G": Keycode.G,
    "H": Keycode.H,
    "I": Keycode.I,
    "J": Keycode.J,
    "K": Keycode.K,
    "L": Keycode.L,
    "M": Keycode.M,
    "N": Keycode.N,
    "O": Keycode.O,
    "P": Keycode.P,
    "Q": Keycode.Q,
    "R": Keycode.R,
    "S": Keycode.S,
    "T": Keycode.T,
    "U": Keycode.U,
    "V": Keycode.V,
    "W": Keycode.W,
    "X": Keycode.X,
    "Y": Keycode.Y,
    "Z": Keycode.Z,
    "F1": Keycode.F1,
    "F2": Keycode.F2,
    "F3": Keycode.F3,
    "F4": Keycode.F4,
    "F5": Keycode.F5,
    "F6": Keycode.F6,
    "F7": Keycode.F7,
    "F8": Keycode.F8,
    "F9": Keycode.F9,
    "F10": Keycode.F10,
    "F11": Keycode.F11,
    "F12": Keycode.F12,
    "F13": Keycode.F13,
    "F14": Keycode.F14,
    "F15": Keycode.F15,
    "F16": Keycode.F16,
    "F17": Keycode.F17,
    "F18": Keycode.F18,
    "F19": Keycode.F19,
    "F20": Keycode.F20,
    "F21": Keycode.F21,
    "F22": Keycode.F22,
    "F23": Keycode.F23,
    "F24": Keycode.F24,
    "DOWN": Keycode.DOWN_ARROW,
    "DOWNARROW": Keycode.DOWN_ARROW,
    "LEFT": Keycode.LEFT_ARROW,
    "LEFTARROW": Keycode.LEFT_ARROW,
    "RIGHT": Keycode.RIGHT_ARROW,
    "RIGHTARROW": Keycode.RIGHT_ARROW,
    "UP": Keycode.UP_ARROW,
    "UPARROW": Keycode.UP_ARROW,
}


# map mouse buttons to mousecodes
mouseButtons = {
    "LEFT": Mouse.LEFT_BUTTON,
    "RIGHT": Mouse.RIGHT_BUTTON,
    "MIDDLE": Mouse.MIDDLE_BUTTON,
}


# map cc commands to consumercontrolcodes
consumerControlCommands = {
    "BRIGHTNESS_DECREMENT": ConsumerControlCode.BRIGHTNESS_DECREMENT,
    "BRIGHTNESS_INCREMENT": ConsumerControlCode.BRIGHTNESS_INCREMENT,
    "EJECT": ConsumerControlCode.EJECT,
    "FAST_FORWARD": ConsumerControlCode.FAST_FORWARD,
    "MUTE": ConsumerControlCode.MUTE,
    "PLAY_PAUSE": ConsumerControlCode.PLAY_PAUSE,
    "RECORD": ConsumerControlCode.RECORD,
    "REWIND": ConsumerControlCode.REWIND,
    "SCAN_NEXT_TRACK": ConsumerControlCode.SCAN_NEXT_TRACK,
    "SCAN_PREVIOUS_TRACK": ConsumerControlCode.SCAN_PREVIOUS_TRACK,
    "STOP": ConsumerControlCode.STOP,
    "VOLUME_DECREMENT": ConsumerControlCode.VOLUME_DECREMENT,
    "VOLUME_INCREMENT": ConsumerControlCode.VOLUME_INCREMENT,
}


# sleep a short amount of time (and add to global delay counter)
def delay(seconds):
    global delayCounter
    time.sleep(seconds)
    delayCounter += seconds


# split string into list tokens and make 1st token UPPERCASE
def splitToTokens(line):
    tokens = line.split(" ")
    tokens[0] = tokens[0].upper()
    return tokens


# join list of tokens to a string
def joinTokens(tokens, start=0):
    return " ".join(tokens[start:])


# pick a random delay time
#  - returns current timestamp and determined delay time
def pickRandomDelay():
    return time.monotonic(), (
        random.randint(
            config["mouseJiggler"]["delayMinimum"],
            config["mouseJiggler"]["delayMaximum"],
        )
    )


# blink onboard LED
def blinkLED(duration=0.2, repeats=1):
    for i in range(repeats):
        led.value = True
        delay(duration)
        led.value = False
        delay(duration)


# infinitely jiggle mouse ever so often
def mouseJigglerLoop():
    # blink LED (startup indicator)
    if config["mouseJiggler"]["LED"]["startupIndicator"]["enabled"]:
        blinkLED(
            config["mouseJiggler"]["LED"]["startupIndicator"]["duration"] / 1000,
            config["mouseJiggler"]["LED"]["startupIndicator"]["repeats"],
        )

    print("")
    print("Running mouse jiggler")
    print("--------------------------------")
    print(" > movement  =", config["mouseJiggler"]["movement"], "pixels")
    print(" > delay min =", config["mouseJiggler"]["delayMinimum"], "seconds")
    print(" > delay max =", config["mouseJiggler"]["delayMaximum"], "seconds")
    print("--------------------------------")

    timestamp, delay = pickRandomDelay()

    print("waiting", delay, "seconds...")
    while True:
        if (time.monotonic() - timestamp) > delay:
            # move mouse up+left then back down+right
            print("jiggling mouse", config["mouseJiggler"]["movement"], "pixels")
            mouse.move(
                x=config["mouseJiggler"]["movement"] * -1,
                y=config["mouseJiggler"]["movement"] * -1,
            )
            mouse.move(
                x=config["mouseJiggler"]["movement"],
                y=config["mouseJiggler"]["movement"],
            )

            # blink LED
            if config["mouseJiggler"]["LED"]["enabled"]:
                blinkLED(config["mouseJiggler"]["LED"]["duration"] / 1000)

            # determine delay
            timestamp, delay = pickRandomDelay()
            print("waiting", delay, "seconds...")


# dynamically load the provided keyboard locale
def loadLocale(locale):
    global KeyboardLayout, Keycode, kbd_layout
    if locale.upper() == "US":
        moduleKeyboardLayout = __import__(
            "adafruit_hid.keyboard_layout_us", globals(), locals(), ["KeyboardLayoutUS"]
        )
        moduleKeycode = __import__(
            "adafruit_hid.keycode", globals(), locals(), ["Keycode"]
        )
        KeyboardLayout = moduleKeyboardLayout.KeyboardLayoutUS
        Keycode = moduleKeycode.Keycode
    else:
        moduleKeyboardLayout = __import__(
            "keyboard_layout_win_" + locale.lower(),
            globals(),
            locals(),
            ["KeyboardLayout"],
        )
        moduleKeycode = __import__(
            "keycode_win_" + locale.lower(), globals(), locals(), ["Keycode"]
        )
        KeyboardLayout = moduleKeyboardLayout.KeyboardLayout
        Keycode = moduleKeycode.Keycode
    kbd_layout = KeyboardLayout(kbd)


# convert to keycodes
def convertLineToKeycodes(line):
    keycodes = []
    # loop on each key - the filter removes empty values
    for key in filter(None, line.split(" ")):
        key = key.upper()
        # find the keycode for the command in the list
        command_keycode = duckyCommands.get(key, None)
        if command_keycode is not None:
            # if it exists in the list, use it
            keycodes.append(command_keycode)
        elif hasattr(Keycode, key):
            # if it's in the Keycode module, use it (allows any valid keycode)
            keycodes.append(getattr(Keycode, key))
        else:
            # if it's not a known key name, show the error for diagnosis
            print(f"Unknown key: <{key}>")
    print(f"{line} (keycodes = {keycodes})")
    return keycodes


# build OR-ed list of mouse buttons to click/press/release
def convertLineToMouseButtons(line):
    buttons = 0
    for button in filter(None, line.split(" ")):
        buttons |= mouseButtons.get(button, None)
    return buttons


# perform a keyboard action (press keys provided in keycode list)
def performKeyboardAction(keycodes):
    for keycode in keycodes:
        kbd.press(keycode)
    kbd.release_all()


# perform a mouse action (move, scroll, click, press, release)
def performMouseAction(line):
    # split line into tokens (0 = command, 1-x = parameters)
    tokens = splitToTokens(line)

    # move mouse pointer
    if tokens[0] == "MOVE":
        moveX = int(tokens[1])
        moveY = int(tokens[2])
        print(f"MOUSE {line} (x={moveX}, y={moveY})")
        mouse.move(x=moveX, y=moveY)

    # scroll mouse wheel
    elif tokens[0] == "WHEEL":
        amount = int(joinTokens(tokens, 1))
        print(f"MOUSE {line}")
        mouse.move(wheel=amount)

    # click and release one or more mouse buttons
    elif tokens[0] == "CLICK":
        mouse_buttons = convertLineToMouseButtons(joinTokens(tokens, 1))
        print(f"MOUSE {line} (buttons = {mouse_buttons})")
        mouse.click(mouse_buttons)

    # press (and don't release) one or more mouse buttons
    elif tokens[0] == "PRESS":
        mouse_buttons = convertLineToMouseButtons(joinTokens(tokens, 1))
        print(f"MOUSE {line} (buttons = {mouse_buttons})")
        mouse.press(mouse_buttons)

    # release one or more mouse buttons
    elif tokens[0] == "RELEASE":
        mouse_buttons = convertLineToMouseButtons(joinTokens(tokens, 1))
        print(f"MOUSE {line} (buttons = {mouse_buttons})")
        mouse.release(mouse_buttons)

    # release all mouse buttons
    elif tokens[0] == "RELEASEALL":
        print(f"MOUSE RELEASEALL")
        mouse.release_all()


# perform a consumer control action
def performConsumerControlAction(line):
    # split line into tokens (0 = command, 1-x = parameters)
    tokens = splitToTokens(line)

    # send cc action
    if tokens[0] == "SEND":
        consumer_code = consumerControlCommands.get(joinTokens(tokens, 1))
        print(f"CC {line} (code = {consumer_code})")
        cc.send(consumer_code)

    # press (and don't release) one or more mouse buttons
    elif tokens[0] == "PRESS":
        consumer_code = consumerControlCommands.get(joinTokens(tokens, 1))
        print(f"CC {line} (code = {consumer_code})")
        cc.press(consumer_code)

    # release currently  pressed cc (only one can be pressed at a time)
    elif tokens[0] == "RELEASE":
        print(f"CC RELEASE")
        cc.release()


# type out provided string
#  - randomly moves mouse in psychoMouse mode
#  - stops time to type out the provided string
def typeString(s):
    prefix = s[0:32] + ("..." if len(s) > 32 else "")
    print(f"STRING {prefix}")
    stopwatch = time.monotonic()

    if psychoMouse:
        rand = []
        for i in range(0, config["psychoMouse"]["randomMovements"]):
            rand.append(
                random.randint(
                    -1 * config["psychoMouse"]["range"], config["psychoMouse"]["range"]
                )
            )
        i = pos = 0
        while pos < len(s):
            kbd_layout.write(s[pos : (pos + config["psychoMouse"]["characters"])])
            mouse.move(
                x=rand[i % config["psychoMouse"]["randomMovements"]],
                y=rand[(i + 1) % config["psychoMouse"]["randomMovements"]],
            )
            i += 1
            pos += config["psychoMouse"]["characters"]
    else:
        kbd_layout.write(s)

    stopwatch = time.monotonic() - stopwatch
    if stopwatch > 1:
        print(f" -> {len(s)} characters in {round(stopwatch, 2)} seconds")
    else:
        print(f" -> {len(s)} characters in {round(1000 * stopwatch, 2)} milliseconds")


# process a line of duckyscript
def processLine(line):
    global defaultDelay, psychoMouse, config

    # split line into tokens (0 = command, 1-x = parameters)
    tokens = splitToTokens(line)

    # comment => ignore them
    if tokens[0] == "REM":
        pass

    # wait X milliseconds
    elif tokens[0] == "DELAY":
        delay(float(tokens[1]) / 1000)

    # output a string directly
    elif tokens[0] == "STRING":
        typeString(joinTokens(tokens, 1))

    # print out statement
    elif tokens[0] == "PRINT":
        print(f"[SCRIPT]: {joinTokens(tokens, 1)}")

    # set default delay
    elif tokens[0] == "DEFAULTDELAY" or tokens[0] == "DEFAULT_DELAY":
        defaultDelay = int(tokens[1]) * 10

    # control the LED
    elif tokens[0] == "LED":
        # toggle if there are not parameters
        if len(tokens) == 1:
            led.value = not led.value
        # enable or disable LED otherwise
        else:
            led.value = True if tokens[1].upper() == "ON" else False

    # control the LED
    elif tokens[0] == "BLINK_LED":
        if len(tokens) == 1:
            blinkLED()
        elif len(tokens) == 2:
            blinkLED(duration=(float(tokens[1]) / 1000))
        elif len(tokens) == 3:
            blinkLED(duration=(float(tokens[1]) / 1000), repeats=float(tokens[2]))

    # import another duckyscript payload
    elif tokens[0] == "IMPORT":
        processDuckyScript(tokens[1], False)

    # switch locale
    elif tokens[0] == "LOCALE":
        loadLocale(tokens[1])

    # control mouse
    elif tokens[0] == "MOUSE":
        performMouseAction(joinTokens(tokens, 1))

    # consumer control command
    elif tokens[0] == "CC":
        performConsumerControlAction(joinTokens(tokens, 1))

    # control psychoMouse mode
    elif tokens[0] == "PSYCHOMOUSE":
        # enable psychoMouse mode
        psychoMouse = True
        if len(tokens) > 1:
            # disable psychoMouse mode
            if tokens[1] == "OFF":
                psychoMouse = False

            # set psychoMouse settings
            else:
                config["psychoMouse"]["characters"] = int(tokens[1])
                if len(tokens) > 2:
                    config["psychoMouse"]["range"] = int(tokens[2])

    # no recognized special command => just run the converted keycodes
    else:
        performKeyboardAction(convertLineToKeycodes(line))


# process a duckyscript file
def processDuckyScript(duckyScriptPath, initialCall=True):
    print("")
    print(f"Running {duckyScriptPath}")
    print("--------------------------------")
    stopwatch = time.monotonic()

    previousLine = ""
    f = open(duckyScriptPath, "r", encoding="utf-8")
    duckyScript = f.readlines()
    for line in duckyScript:

        # split line into tokens (0 = command, 1-x = parameters)
        line = line.rstrip()
        tokens = splitToTokens(line)

        if tokens[0] == "REPEAT":
            # repeat the last command
            for i in range(int(tokens[1])):
                processLine(previousLine)
                delay(float(defaultDelay) / 1000)
        else:
            processLine(line)
            previousLine = line
        delay(float(defaultDelay) / 1000)

    print("--------------------------------")

    stopwatch = time.monotonic() - stopwatch
    if stopwatch > 1:
        print(
            f" -> Finished {duckyScriptPath}. Processed {len(duckyScript)} lines in {round(stopwatch, 2)} seconds."
        )
    else:
        print(
            f" -> Finished {duckyScriptPath}. Processed {len(duckyScript)} lines in {round(1000 * stopwatch, 2)} milliseconds."
        )
    if initialCall:
        print(
            f" -> All delays (commands and default delay) summed up to {delayCounter} seconds."
        )
    print("")


# check if provided pin is grounded
def isPinGrounded(pin):
    checkPin = DigitalInOut(pin)
    checkPin.switch_to_input(pull=Pull.UP)
    return not checkPin.value


# set up keyboard + mouse
kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
loadLocale(config["locale"])

# set up LED
led = DigitalInOut(LED)
led.direction = Direction.OUTPUT

# default settings
defaultDelay = config["defaultDelay"]
psychoMouse = False
delayCounter = 0

# sleep at the start to allow the device to be recognized by the host computer
time.sleep(config["initialSleep"] / 1000)

# check GP0/GP1/GP2/GP3/GP4/GP5/GP6 for run mode
if isPinGrounded(GP0):
    processDuckyScript(config["payloads"]["GP0"])
elif isPinGrounded(GP1):
    processDuckyScript(config["payloads"]["GP1"])
elif isPinGrounded(GP2):
    processDuckyScript(config["payloads"]["GP2"])
elif isPinGrounded(GP3):
    processDuckyScript(config["payloads"]["GP3"])
elif isPinGrounded(GP4):
    processDuckyScript(config["payloads"]["GP4"])
elif isPinGrounded(GP5):
    processDuckyScript(config["payloads"]["GP5"])
elif isPinGrounded(GP6):
    mouseJigglerLoop()
else:
    print(
        "You're in setup mode. Update your payload(s) and ground the corresponding pin (GP0-GP5) to run one of them afterwards."
    )
