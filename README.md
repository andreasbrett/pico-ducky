<h1>This is a fork...</h1>

This is a fork of [dbisu's pico-ducky](https://github.com/dbisu/pico-ducky). Additions to the original code...

- introducing new commands to the Ducky Script language (see below)
- allowing to run one of 6 different payloads (by grounding pins `GP0`, `GP1`, `GP2`, `GP3`, `GP4` or `GP5`)
- allowing to run a mouse jiggler when grounding `GP6` (see Hak5 presentation: https://www.youtube.com/watch?v=aZ8u56I3J3I)

Changes to the Ducky Script language are:

- importing other payloads through e.g. `IMPORT filename.dd`
- setting keyboard locale __at runtime__ through e.g. `LOCALE DE` (which would load `keyboard_layout_win_de` and `keycode_win_de` from the libs folder).
- sending mouse commands (movements, wheel action, clicks, presses and releases)
  - `MOUSE MOVE $x $y` - moves the mouse pointer
  - `MOUSE WHEEL $amount` - moves the mouse wheel (negative = toward the user, positive = away from the user)
  - `MOUSE CLICK/PRESS/RELEASE LEFT [RIGHT] [MIDDLE]` - click, press or release one ore more buttons (e.g. `MOUSE PRESS LEFT RIGHT` would keep the left and right buttons pressed until issuing a `MOUSE RELEASE LEFT RIGHT` or `MOUSE RELEASEALL` command)
  - `MOUSE RELEASEALL` - releases all pressed buttons
  - these work great in scenarios where you want to mess with user's ability to e.g. close your shell by moving the mouse or to spookily move the mouse around ever so often
- activating <strong>psycho-mouse</strong> mode through `PSYCHOMOUSE [CHARS] [RANGE]`
  - this mode will randomly move the mouse when typing strings from a `STRING $yourstring` command
  - user won't be able to close your shell by mouse (we all know lusers don't know keyboard shortcuts)
  - `PSYCHOMOUSE` will activate psycho-mouse mode with default values (chars = 5, range = 250)
  - `PSYCHOMOUSE 12 300` moves mouse every 12 chars in a range of +/- 300 pixels
  - `PSYCHOMOUSE OFF` disables psycho-mouse mode
  - <strong>note:</strong> typing performance reduces by roughly 10% with the default value for `chars=5`

<h1 align="center">pico-ducky</h1>

<div align="center">
  <strong>Make a cheap but powerful USB Rubber Ducky with a Raspberry Pi Pico</strong>
</div>

<br />

<div align="center">
  <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/dbisu/pico-ducky">
  <img alt="GitHub license" src="https://img.shields.io/github/license/dbisu/pico-ducky">
  <a href="https://github.com/dbisu/pico-ducky/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/dbisu/pico-ducky"></a>
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/dbisu/pico-ducky">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/dbisu/pico-ducky">
</div>

<br />

## Install

Install and have your USB Rubber Ducky working in less than 5 minutes.

1. Download [CircuitPython for the Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/). *Updated to 7.0.0

2. Plug the device into a USB port while holding the boot button. It will show up as a removable media device named `RPI-RP2`.

3. Copy the downloaded `.uf2` file to the root of the Pico (`RPI-RP2`). The device will reboot and after a second or so, it will reconnect as `CIRCUITPY`.

4. Download `adafruit-circuitpython-bundle-7.x-mpy-YYYYMMDD.zip` [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/latest) and extract it outside the device.

5. Navigate to `lib` in the recently extracted folder and copy `adafruit_hid` to the `lib` folder in your Raspberry Pi Pico.

6. Click [here](https://raw.githubusercontent.com/dbisu/pico-ducky/main/duckyinpython.py), press CTRL + S and save the file as `code.py` in the root of the Raspberry Pi Pico, overwriting the previous file.

7. Find a script [here](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads) or [create your own one using Ducky Script](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript) and save it as `payload0.dd` on the Pico.

8. To run this payload connect pin 1 (`GP0`) to pin 3 (`GND`) and re-plug the pico. It will reboot and after half a second, the script will run.

### Run vs Setup mode

Select which payload should be run by grounding either pin 1 (`GP0`), pin 2 (`GP1`), pin 4 (`GP3`), pin 5 (`GP4`) or pin 6 (`GP5`) to the ground pin 3 (`GND`). This will tell pico-ducky which of the 6 payload files to run. The easiest way to do so is by using a jumper wire between those pins as seen below (in this case `GP0` is grounded therefore `payload0.dd` will be run). If neither pin is grounded, pico-ducky will be in setup-mode and execute no payload. You are then free to modify your script without risking injecting any payloads.

![Setup mode with a jumper](images/setup-mode.png)

### USB enable/disable mode

If you need the pico-ducky to not show up as a USB mass storage device for stealth, follow these instructions.  
Enter setup mode.  
Copy boot.py to the root of the pico-ducky.  
Copy your payload script to the pico-ducky.  
Disconnect the pico from your host PC.
Connect a jumper wire between pin 18 and pin 20.
This will prevent the pico-ducky from showing up as a USB drive when plugged into the target computer.  
Remove the jumper and reconnect to your PC to reprogram.
The default mode is USB mass storage enabled.   

![USB enable/disable mode](images/usb-boot-mode.png)

### Changing Keyboard Layouts

Copied from [Neradoc/Circuitpython_Keyboard_Layouts](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/blob/main/PICODUCKY.md)  

#### How to use one of these layouts with the pico-ducky repository.

**Go to the [latest release page](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/releases/latest), look if your language is in the list.**

#### If your language/layout is in the bundle

Download the `py` zip, named `circuitpython-keyboard-layouts-py-XXXXXXXX.zip`

**NOTE: You can use the mpy version targetting the version of Circuitpython that is on the device, but on Raspberry Pi Pico you don't need it - they only reduce file size and memory use on load, which the pico has plenty of.**

#### If your language/layout is not in the bundle

Try the online generator, it should get you a zip file with the bundles for yout language

https://www.neradoc.me/layouts/

#### Now you have a zip file

#### Find your language/layout in the lib directory

For a language `LANG`, copy the following files from the zip's `lib` folder to the `lib` directory of the board.  
**DO NOT** modify the adafruit_hid directory. Your files go directly in `lib`.  
**DO NOT** change the names or extensions of the files. Just pick the right ones.  
Replace `LANG` with the letters for your language of choice.

- `keyboard_layout.py`
- `keyboard_layout_win_LANG.py`
- `keycode_win_LANG.py`

Don't forget to get [the adafruit_hid library](https://github.com/adafruit/Adafruit_CircuitPython_HID/releases/latest).

This is what it should look like **if your language is French for example**.

![CIRCUITPY drive screenshot](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/raw/main/docs/drive_pico_ducky.png)

#### Modify the pico-ducky code to use your language file:

At the start of the file comment out these lines:

```py
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
```

Uncomment these lines:  
*Replace `LANG` with the letters for your language of choice. The name must match the file (without the py or mpy extension).*
```py
from keyboard_layout_win_LANG import KeyboardLayout
from keycode_win_LANG import Keycode
```

## Useful links and resources

### Docs

[CircuitPython](https://circuitpython.readthedocs.io/en/6.3.x/README.html)

[CircuitPython HID](https://learn.adafruit.com/circuitpython-essentials/circuitpython-hid-keyboard-and-mouse)

[Ducky Script](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript)

### Video tutorials

[pico-ducky tutorial by **NetworkChuck**](https://www.youtube.com/watch?v=e_f9p-_JWZw)

[USB Rubber Ducky playlist by **Hak5**](https://www.youtube.com/playlist?list=PLW5y1tjAOzI0YaJslcjcI4zKI366tMBYk)

[CircuitPython tutorial on the Raspberry Pi Pico by **DroneBot Workshop**](https://www.youtube.com/watch?v=07vG-_CcDG0)
