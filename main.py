# Software for Digital Stylophone project
# Made by Gamufal
# Version: 25.9.1

from machine import Pin, ADC, I2C, PWM
import ssd1306
import json
from time import sleep, time, ticks_ms, ticks_diff

# Initialization of OLED Display (128x64)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# LED diode initialization
led = Pin(13, Pin.OUT)

# Buttons initialization 
btn_down  = Pin(6,  Pin.IN, Pin.PULL_UP)
btn_up    = Pin(8,  Pin.IN, Pin.PULL_UP)
btn_right = Pin(7,  Pin.IN, Pin.PULL_UP)
btn_left  = Pin(9,  Pin.IN, Pin.PULL_UP)
btn_ok    = Pin(10, Pin.IN, Pin.PULL_UP)

# ADC Initialization for stylus 
adc = ADC(Pin(26))
adc_thresholds = [4500, 9000, 13000, 17000, 20000, 24000, 29000, 34000, 39000, 46000, 54000, 64000]

# PWM Initialization for the speaker
spk = PWM(Pin(16))
spk.duty_u16(0)

# Three sets of notes:
lower_octave  = [131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247]
middle_octave = [261, 277, 293, 311, 329, 349, 369, 392, 415, 440, 466, 493]
higher_octave = [523, 554, 587, 622, 659, 698, 739, 784, 830, 880, 932, 987]

# Global settings
volume = 4   # 1-8
tone = 2     # 1-3
recording = []  # (freq, timestamp), ...

# Saves a single setting to a JSON file
def save_single_setting(key, value):
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except (OSError, ValueError):
        settings = {}
    settings[key] = value
    with open("settings.json", "w") as f:
        json.dump(settings, f)
    print(f"Saved {key}: {value}")

# Loads saved settings from a JSON file
def load_settings():
    global volume, tone, recording
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            volume = settings.get("volume", 4)
            tone = settings.get("tone", 2) 
            recording = settings.get("recording", [])  
        print("Settings loaded!")
    except Exception as e:
        print("No settings found, using defaults.", e)

# Returns the index of the note based on the ADC value
def get_note_index(adc_val):
    idx = -1
    for i in range(len(adc_thresholds)):
        if adc_val >= adc_thresholds[i]:
            idx = i
        else:
            break
    return idx if idx != -1 else None

# Retrieves the note frequency from the index and currently selected octave
def get_note_from_index(idx):
    global tone
    if tone == 1:
        return lower_octave[idx]
    elif tone == 2:
        return middle_octave[idx]
    elif tone == 3:
        return higher_octave[idx]

# Updates the speaker output in real time based on the ADC reading
def update_live_audio():
    adc_val = adc.read_u16()
    idx = get_note_index(adc_val)
    if idx is not None:
        freq = get_note_from_index(idx)
        spk.freq(freq)
        spk.duty_u16(volume * 4096)
    else:
        spk.duty_u16(0)

# Displays the main menu
def display_menu(selected_item):
    menu_items = ["VOLUME", "TONE", "RECORD", "PLAY"]
    display.fill(0)
    for i, item in enumerate(menu_items):
        y = i * 16
        if i == selected_item:
            display.fill_rect(0, y, 128, 16, 1)  
            display.text(item, 16, y + 4, 0)      
        else:
            display.text(item, 16, y + 4, 1)      
    display.show()

# Handles volume adjustment
def volume_menu():
    global volume
    display.fill(0)
    display.text("VOLUME", 16, 30, 1)
    display.text(str(volume), 104, 30, 1)
    bar_width = int(volume * 96 / 8)
    display.fill_rect(16, 45, bar_width, 10, 1)
    display.show()
    while True:
        update_live_audio()
        if btn_left.value() == 0 and volume > 1:
            volume -= 1
            display.fill(0)
            display.text("VOLUME", 16, 30, 1)
            display.text(str(volume), 104, 30, 1)
            bar_width = int(volume * 96 / 8)
            display.fill_rect(16, 45, bar_width, 10, 1)
            display.show()
            sleep(0.2)
        elif btn_right.value() == 0 and volume < 8:
            volume += 1
            display.fill(0)
            display.text("VOLUME", 16, 30, 1)
            display.text(str(volume), 104, 30, 1)
            bar_width = int(volume * 96 / 8)
            display.fill_rect(16, 45, bar_width, 10, 1)
            display.show()
            sleep(0.2)
        elif btn_up.value() == 0 or btn_down.value() == 0:
            save_single_setting("volume", volume)
            while btn_up.value() == 0 or btn_down.value() == 0:      
                sleep(0.05)
            return
        sleep(0.05)

# Handles octaves selection
def tone_menu():
    global tone
    display.fill(0)
    display.text("TONE", 16, 30, 1)
    display.text(str(tone), 104, 30, 1)
    bar_width = int(tone * 96 / 3)  
    display.fill_rect(16, 45, bar_width, 10, 1)
    display.show()
    while True:
        update_live_audio()
        if btn_left.value() == 0 and tone > 1:
            tone -= 1
            display.fill(0)
            display.text("TONE", 16, 30, 1)
            display.text(str(tone), 104, 30, 1)
            bar_width = int(tone * 96 / 3)  
            display.fill_rect(16, 45, bar_width, 10, 1)
            display.show()
            sleep(0.2)
        elif btn_right.value() == 0 and tone < 3:
            tone += 1
            display.fill(0)
            display.text("TONE", 16, 30, 1)
            display.text(str(tone), 104, 30, 1)
            bar_width = int(tone * 96 / 3)  
            display.fill_rect(16, 45, bar_width, 10, 1)
            display.show()
            sleep(0.2)
        elif btn_up.value() == 0 or btn_down.value() == 0:
            save_single_setting("tone", tone)
            while btn_up.value() == 0 or btn_down.value() == 0:
                sleep(0.05)
            return
        sleep(0.05)

# Records a sequence of note frequencies
def record_menu():
    global recording
    display.fill(0)
    display.text("RECORD", 16, 30, 1)
    display.text("OK = start", 16, 42, 1)
    display.show()
    while True:
        update_live_audio()
        if btn_ok.value() == 0:
            while btn_ok.value() == 0:
                sleep(0.05)
            display.fill(0)
            display.text("Recording...", 16, 30, 1)
            display.show()
            print("Waiting for first note...")
            while True:
                adc_val = adc.read_u16()
                idx = get_note_index(adc_val)
                if idx is not None:
                    break
                sleep(0.05)
            recording = []
            start_time = ticks_ms()
            last_led_toggle = ticks_ms()
            while True:
                adc_val = adc.read_u16()
                idx = get_note_index(adc_val)
                if idx is None:
                    freq = 0
                    spk.duty_u16(0)
                else:
                    freq = get_note_from_index(idx)
                    spk.freq(freq)
                    spk.duty_u16(volume * 4096)
                    print("Recording note:", freq)
                current_time = ticks_diff(ticks_ms(), start_time)
                recording.append((freq, current_time))
                if ticks_diff(ticks_ms(), last_led_toggle) >= 500:
                    led.value(not led.value())
                    last_led_toggle = ticks_ms()
                if btn_ok.value() == 0:
                    while btn_ok.value() == 0:
                        sleep(0.05)
                    break
                sleep(0.01)
            spk.duty_u16(0)
            led.off()
            save_single_setting("recording", recording)
            display.fill(0)
            display.text("Done", 16, 30, 1)
            display.show()
            sleep(1)
            return
        elif btn_up.value() == 0 or btn_down.value() == 0:
            while btn_up.value() == 0 or btn_down.value() == 0:
                sleep(0.05)
            return
        sleep(0.05)

# Plays back a previously recorded track
def play_menu():
    display.fill(0)
    display.text("PLAY", 16, 30, 1)
    display.text("OK = play", 16, 42, 1)
    display.show()
    while True:
        update_live_audio()
        if btn_ok.value() == 0:
            while btn_ok.value() == 0:
                sleep(0.05)
            display.fill(0)
            display.text("Playing...", 16, 30, 1)
            display.show()
            led.on()
            start_play = ticks_ms()
            for i in range(len(recording) - 1):
                freq, t = recording[i]
                next_freq, next_t = recording[i+1]
                if freq != 0:
                    spk.freq(freq)
                    spk.duty_u16(volume * 4096)
                    print("Playing note:", freq, "for", (next_t - t)/1000, "s")
                else:
                    spk.duty_u16(0)
                    print("Playing silence for", (next_t - t)/1000, "s")
                delay_ms = next_t - t
                sleep(delay_ms / 1000)
            spk.duty_u16(0)
            led.off()
            display.fill(0)
            display.text("OK = play", 16, 30, 1)
            display.show()
            return
        elif btn_up.value() == 0 or btn_down.value() == 0:
            while btn_up.value() == 0 or btn_down.value() == 0:
                sleep(0.05)
            return
        sleep(0.05)

# Main loop
def main():
    selected_item = 0
    while True:
        display_menu(selected_item)
        update_live_audio()
        if btn_down.value() == 0:
            selected_item = (selected_item + 1) % 4
            sleep(0.2)
        if btn_up.value() == 0:
            selected_item = (selected_item - 1) % 4
            sleep(0.2)
        if btn_ok.value() == 0:
            while btn_ok.value() == 0:
                sleep(0.05)
            if selected_item == 0:
                volume_menu()
            elif selected_item == 1:
                tone_menu()
            elif selected_item == 2:
                record_menu()
            elif selected_item == 3:
                play_menu()
        sleep(0.05)

# Program start
load_settings()
main()

