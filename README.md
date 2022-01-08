<h1>This is a fork...</h1>

This is a fork of [dbisu's pico-ducky](https://github.com/dbisu/pico-ducky). Apart from major refactoring, additions to the original code are as follows:

-   introduced new commands to the Ducky Script language (see below)
-   beautified serial output
    -   easier to debug, better to analyze scripts
    -   performance of scripts is now measured
    -   it's easy to compare how much enabling e.g. `PSYCHOMOUSE` mode affects performance (spoiler: roughly 15-20%)
-   separate configuration file to customize your pico-ducky
    -   many hard-coded settings of the original pico-ducky can now be configured
    -   use template `pd\config_default.py` and store it as `pd\config.py` for custom settings
-   allows running one of 6 different payloads (by grounding pins `GP0`, `GP1`, `GP2`, `GP3`, `GP4` or `GP5`)
-   allows running a mouse jiggler when grounding `GP6` (see Hak5 presentation: https://www.youtube.com/watch?v=aZ8u56I3J3I)
-   includes some basic duckyscripts to get you started in folder `pd`

Changes to the Ducky Script language are:

-   importing other payloads through e.g. `IMPORT filename.dd`
-   setting keyboard locale **at runtime** through e.g. `LOCALE DE` (which would load `keyboard_layout_win_de` and `keycode_win_de` from the libs folder).
-   wait for keyboard LED to be on or off
    -   `WAITFORLED CAPS_LOCK ON`
    -   `WAITFORLED NUM_LOCK OFF`
    -   `WAITFORLED SCROLL_LOCK ON`
    -   `WAITFORLED COMPOSE ON`
    -   LED states are polled every 100ms, so also quick key presses are caught
    -   great to build trigger patterns (e.g. NUM on, NUM off, CAPS on, CAPS off)
-   blinking LED through e.g.
    -   `BLINK_LED` (blink once with default duration)
    -   `BLINK_LED 250` (blink once for 250ms)
    -   `BLINK_LED 500 3` (blink 3x for 500ms)
-   all F-keys can be sent (so also F13-F24)
-   added commands
    -   `RIGHTALT`
    -   `RIGHTCONTROL`
    -   `RIGHTGUI`
    -   `RIGHTSHIFT`
    -   `POWER` (specific to MacOS)
-   sending consumer control commands (aka media keys)
    -   `CC SEND BRIGHTNESS_DECREMENT`
    -   `CC SEND BRIGHTNESS_INCREMENT`
    -   `CC SEND EJECT`
    -   `CC SEND FAST_FORWARD`
    -   `CC SEND MUTE`
    -   `CC SEND PLAY_PAUSE`
    -   `CC SEND RECORD`
    -   `CC SEND REWIND`
    -   `CC SEND SCAN_NEXT_TRACK`
    -   `CC SEND SCAN_PREVIOUS_TRACK`
    -   `CC SEND STOP`
    -   `CC SEND VOLUME_DECREMENT`
    -   `CC SEND VOLUME_INCREMENT`
    -   to press and later release a media key use the following commands (only one can be pressed at a time!)
        -   `CC PRESS VOLUME_INCREMENT`
        -   `CC RELEASE`
-   sending mouse commands (movements, scrollwheel action, clicks, presses and releases)
    -   `MOUSE MOVE $x $y` - moves the mouse pointer
    -   `MOUSE WHEEL $amount` - moves the mouse wheel (negative = toward the user, positive = away from the user)
    -   `MOUSE CLICK/PRESS/RELEASE LEFT [RIGHT] [MIDDLE]` - click, press or release one ore more buttons
        -   `MOUSE CLICK RIGHT` presses and immediately releases the right button
        -   `MOUSE PRESS LEFT RIGHT` keeps the left and right buttons pressed
        -   `MOUSE RELEASE LEFT RIGHT` releases them again
    -   `MOUSE RELEASEALL` - releases all pressed buttons
    -   these work great in scenarios where you want to mess with user's ability to e.g. close your shell by moving the mouse or to spookily move the mouse around ever so often
-   activating <strong>psycho-mouse</strong> mode through `PSYCHOMOUSE [CHARS] [RANGE]`
    -   this mode will randomly move the mouse when issuing a `STRING $yourstring` command
    -   user won't be able to close your shell by mouse (we all know lusers don't know keyboard shortcuts)
    -   `PSYCHOMOUSE` will activate psycho-mouse mode with default values (chars = 5, range = 250)
    -   `PSYCHOMOUSE 12 300` moves mouse every 12 chars in a range of +/- 300 pixels
    -   `PSYCHOMOUSE OFF` disables psycho-mouse mode
    -   <strong>note:</strong> typing performance reduces by roughly 15-20% with the default values

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

1. Download [CircuitPython for the Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/). \*Updated to 7.0.0

2. Plug the device into a USB port while holding the boot button. It will show up as a removable media device named `RPI-RP2`.

3. Copy the downloaded `.uf2` file to the root of the Pico (`RPI-RP2`). The device will reboot and after a second or so, it will reconnect as `CIRCUITPY`.

4. Download `adafruit-circuitpython-bundle-7.x-mpy-YYYYMMDD.zip` [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/latest) and extract it outside the device.

5. Navigate to `lib` in the recently extracted folder and copy `adafruit_hid` to the `lib` folder in your Raspberry Pi Pico.

6. Place `boot.py`, `main.py` and folder `pd` in the root of the Raspberry Pi Pico, overwriting previous files.

7. Find a script [here](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payloads) or [create your own one using Ducky Script](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript) and save it as `pd\payload0.dd` on the Pico.

8. To run this payload connect pin 1 (`GP0`) to pin 3 (`GND`) and re-plug the pico. It will reboot and after half a second, the script will run.

9. To tweak how the pico-ducky works copy `pd\config_default.py` to `pd\config.py` and customize the settings to fit your needs.

### Run vs Setup mode

Select which payload should be run by grounding either pin 1 (`GP0`), pin 2 (`GP1`), pin 4 (`GP3`), pin 5 (`GP4`) or pin 6 (`GP5`) to the ground pin 3 (`GND`). This will tell pico-ducky which of the 6 payload files to run. The easiest way to do so is by using a jumper wire between those pins as seen below (in this case `GP0` is grounded therefore `payload0.dd` in folder `pd` will be run). If neither pin is grounded, pico-ducky will be in setup-mode and execute no payload. You are then free to modify your script without risking injecting any payloads.

![Setup mode with a jumper](images/setup-mode.png)

### USB enable/disable mode

If you need the pico-ducky to not show up as a USB mass storage device for stealth, simply ground pins 18 (`GND`) and pin 20 (`GP15`). This will prevent the pico-ducky from showing up as a USB drive when plugged into the target computer. Remove the jumper and reconnect to your PC to reprogram.

By default USB mass storage is enabled.

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

-   `keyboard_layout.py`
-   `keyboard_layout_win_LANG.py`
-   `keycode_win_LANG.py`

Don't forget to get [the adafruit_hid library](https://github.com/adafruit/Adafruit_CircuitPython_HID/releases/latest).

This is what it should look like **if your language is French for example**.

![CIRCUITPY drive screenshot](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/raw/main/docs/drive_pico_ducky.png)

#### Modify the pico-ducky code to use your language file:

Re-configure the locale pico-ducky should use by default in the provided `pd\config_default.py`. You could also dynamically use the `LOCALE` command to change your locale at runtime (e.g. start your duckyscripts with `LOCALE DE` for a german keyboard)

## Useful links and resources

### Docs

[CircuitPython](https://circuitpython.readthedocs.io/en/6.3.x/README.html)

[CircuitPython HID](https://learn.adafruit.com/circuitpython-essentials/circuitpython-hid-keyboard-and-mouse)

[Ducky Script](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript)

### Video tutorials

[pico-ducky tutorial by **NetworkChuck**](https://www.youtube.com/watch?v=e_f9p-_JWZw)

[USB Rubber Ducky playlist by **Hak5**](https://www.youtube.com/playlist?list=PLW5y1tjAOzI0YaJslcjcI4zKI366tMBYk)

[CircuitPython tutorial on the Raspberry Pi Pico by **DroneBot Workshop**](https://www.youtube.com/watch?v=07vG-_CcDG0)
