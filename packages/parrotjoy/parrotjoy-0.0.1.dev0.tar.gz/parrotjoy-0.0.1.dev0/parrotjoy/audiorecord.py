"""Recording audio and doing some analysis on it as we go.
"""

from queue import Queue

import numpy as np
import aubio
import pygame as pg
from pygame.midi import (
    midi_to_frequency,
    midi_to_ansi_note,
)

pygame = pg

from pygame._sdl2 import (
    AUDIO_F32,
    get_audio_device_names,
    AudioDevice,
    AUDIO_ALLOW_FORMAT_CHANGE,
)

AUDIOS = pg.event.custom_type()
ONSETS = pg.event.custom_type()
PITCHES = pg.event.custom_type()


class AudioRecord:
    """Recording audio and doing some analysis on it as we go.

    It looks for onsets (beats), pitch detection (notes, and midi frequencies)
    """

    def __init__(self, inputdevice):
        self.inputdevice = inputdevice
        self.audio_going = True
        self.onset_queue = Queue()
        self.audio_queue = Queue()
        self.pitch_queue = Queue()

        self.callback = lambda audiodevice, stream: self.on_data(audiodevice, stream)

    def update(self):
        """To be called in a pygame event loop."""
        audios = []
        while not self.audio_queue.empty():
            # print('-----audio from queue')
            # print(time.time() - time_start)
            audio = self.audio_queue.get()
            audios.append(audio)

        if audios:
            pg.event.post(pg.event.Event(AUDIOS, audios=audios))

        onsets = []
        while not self.onset_queue.empty():
            onsets.append(self.onset_queue.get())

        if onsets:
            pg.event.post(pg.event.Event(ONSETS, onsets=onsets))

        pitches = []
        notes = []
        frequencies = []
        while not self.pitch_queue.empty():

            # print("pitch, confidence", pitch, confidence, midi_to_ansi_note(pitch))
            pitch = self.pitch_queue.get()
            pitches.append(pitch)
            notes.append(midi_to_ansi_note(pitch))
            frequencies.append(midi_to_frequency(pitch))

        if pitches:
            pg.event.post(
                pg.event.Event(
                    PITCHES, pitches=pitches, notes=notes, frequencies=frequencies
                )
            )

    def on_data(self, audiodevice, audiobuffer):
        self.audio_queue.put(bytes(audiobuffer))
        # print(type(audiobuffer), len(audiobuffer))
        signal = np.frombuffer(audiobuffer, dtype=np.float32)
        # print(audiodevice)
        onset = self.onset(signal)
        if onset > 1:
            # print("%f" % self.onset.get_last_s())
            self.onset_queue.put(True)

        pitch = self.pitch_o(signal)[0]
        # pitch = int(round(pitch))
        if int(round(pitch)):
            confidence = self.pitch_o.get_confidence()
            # print("pitch, confidence", pitch, confidence, midi_to_ansi_note(pitch))
            self.pitch_queue.put(pitch)

    def start(self):
        FORMAT = AUDIO_F32
        CHANNELS = 1
        RATE = 44100
        CHUNK = 512

        just_names = get_audio_device_names(iscapture=1)
        print(just_names)
        devicename = (
            self.inputdevice if self.inputdevice in just_names else just_names[0]
        )
        print(f"Using: {devicename}")

        # onset detection.
        win_s = 1024
        hop_s = win_s // 2
        self.onset = aubio.onset("default", win_s, hop_s, RATE)

        tolerance = 0.8
        self.pitch_o = aubio.pitch("yin", win_s, hop_s, RATE)
        self.pitch_o.set_unit("midi")
        self.pitch_o.set_tolerance(tolerance)

        self.audio_device = AudioDevice(
            devicename=devicename,
            iscapture=1,
            frequency=RATE,
            audioformat=AUDIO_F32,
            numchannels=CHANNELS,
            chunksize=CHUNK,
            allowed_changes=AUDIO_ALLOW_FORMAT_CHANGE,
            callback=self.callback,
        )

        self.audio_device.pause(0)

    def __del__(self):
        self.audio_device.pause(1)
        self.audio_device.close()
