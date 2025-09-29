# Digital Stylophone

A microcontroller-based stylophone with recording and playback capabilities, built around the Raspberry Pi Pico. This project reimagines the classic analog instrument with modern digital features, including an OLED display and non-volatile memory for storing recorded tracks.

## Demo

![Digital Stylophone](https://github.com/Gamufal/DigitalStyphone/blob/main/prototype.png?raw=true)


## Features

*   **Sound Generation:** Produces a square wave tone with a classic synthesizer sound.
*   **Multiple Octaves:** Three selectable octaves (low, middle, high).
*   **Volume Control:** Adjustable volume with 8 levels.
*   **Recording & Playback:** Record, save, and play back musical sequences.
*   **Persistent Memory:** Saves the recorded track and user settings (volume, octave) to a `settings.json` file on the device.
*   **OLED Display Interface:** A 128x64 SSD1306 OLED screen provides a menu-based interface for all functions.
*   **Tactile Controls:** 5-button navigation for intuitive menu control.
*   **Portable Design:** Powered by a 9V battery for on-the-go use.
*   **Raspberry Pi Pico Core:** Utilizes a Raspberry Pi Pico for all processing and hardware control.

## Hardware

### Components

| Component | Quantity |
|---|---|
| Raspberry Pi Pico | 1 |
| 5mm LED | 2 |
| 1kΩ Resistor (1/4W) | 21 |
| 10kΩ Resistor (1/4W) | 1 |
| 0.96" OLED Display | 1 |
| LM2596 Step-down Converter | 1 |
| 6x6mm Tactile Switch | 5 |
| Female Pin Headers | 5 |
| Latching Switch | 1 |
| 9V Battery | 1 |
| 1W 8Ohm Speaker | 1 |

### Schematic

![Schematic](https://github.com/Gamufal/DigitalStyphone/blob/main/schematic.png?raw=true)

### PCB Layout

![PCB Layout](https://github.com/Gamufal/DigitalStyphone/blob/main/PCB-layout.png?raw=true)

## Software

### How it Works

The device is controlled by a MicroPython script (`main.py`) running on the Raspberry Pi Pico.

*   **Sound Generation:** The stylus's position on the resistive keyboard is read as an analog value by the Pico's ADC (Analog-to-Digital Converter). This value is then mapped to a specific musical note frequency. The sound is generated using PWM (Pulse Width Modulation) sent to a 1W speaker.

*   **UI & Menu:** A menu-driven interface is displayed on the 128x64 OLED screen. The user navigates the menu using a 5-button keypad. The available options are Volume, Tone (Octave), Record, and Play.

*   **Recording & Playback:** The recording function captures a sequence of notes and their timings. It records pairs of `(frequency, timestamp)` to a list. The playback function iterates through the recorded list, playing back the notes with the correct timing.

*   **Persistence:** The recorded song, as well as the volume and tone settings, are saved to a `settings.json` file in the Pico's flash memory. This allows the device to retain settings and recordings between power cycles.

### Installation

1.  **Install MicroPython:** If you haven't already, install MicroPython on your Raspberry Pi Pico. You can find the official instructions [here](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).

2.  **Install `ssd1306.py`:** The OLED display requires the `ssd1306.py` library. You can find it [here](https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py) and save it to your Pico.

3.  **Upload the Software:** Copy the `main.py` file to your Raspberry Pi Pico. The easiest way to do this is by using an IDE like [Thonny](https://thonny.org/), which has a simple interface for managing files on a MicroPython device.

## User Guide

### Controls

| Control | Function |
|---|---|
| Up/Down Buttons | Navigate through the main menu. |
| Left/Right Buttons | Decrease/increase the volume or tone (octave). |
| OK Button | Select a menu option; start/stop recording or playback. |
| Stylus | Play notes by touching the corresponding keys. |

### Operation

1.  **Power On:** Connect a 9V battery and flip the power switch. The green LED will light up, and the main menu will appear on the OLED display.
2.  **Play Music:** Simply touch the stylus to any of the metal keys to play a note.
3.  **Navigate Menu:** Use the **Up** and **Down** buttons to highlight a menu option.
4.  **Select Option:** Press the **OK** button to enter the selected menu (Volume, Tone, Record, or Play).
5.  **Adjust Volume/Tone:** In the Volume or Tone menus, use the **Left** and **Right** buttons to make adjustments. Press **Up** or **Down** to exit and save.
6.  **Record:** Select "RECORD" from the main menu and press **OK**. Press **OK** again to start recording. The red LED will blink. Play your tune, and press **OK** to stop. The recording will be saved automatically.
7.  **Playback:** Select "PLAY" from the main menu and press **OK**. Press **OK** again to start playback of the last recorded track. The red LED will stay lit during playback.

## Troubleshooting

| Symptom | Possible Cause | Suggested Solution |
|---|---|---|
| Screen works, but the green power LED is off. | The green LED is burnt out. | Replace the green LED. |
| The green power LED is on, but the screen is blank. | The OLED display is damaged or disconnected. | Check the display's connections. If the problem persists, replace the display module. |
| Nothing works (no screen, no LEDs). | The 9V battery is dead. | Replace the 9V battery. |
| The screen and LEDs work, but there is no sound. | The speaker is damaged or disconnected. | Check the speaker wiring. If the problem persists, replace the speaker. |

## Future Improvements

*   **Enhanced Sound Engine:**
    *   Add a vibrato effect using a Low-Frequency Oscillator (LFO).
*   **Connectivity:**
    *   Add MIDI output via USB, allowing the stylophone to function as a MIDI controller.
*   **Code Refinements:**
    *   Refactor the code for better efficiency, especially the recording and display update logic.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
