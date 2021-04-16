#!/usr/bin/env python3

import asyncio
import evdev
import evdev.ecodes as ecodes

"""
This mapping is for the Acme editor. It just makes both side buttons
(BTN_SIDE and BTN_EXTRA) behave like the wheel button, so it's
easier to press, drag, and chord.
"""

# Listen to events from the mouse
# TODO Implement mouse finder (right now upon every boot
# I have to search for it manually)
mouse = evdev.InputDevice("/dev/input/event9")   # /dev/input/event?

# Create virtual mouse
virtual_mouse = evdev.UInput.from_device(mouse, name="virtual-mouse")

# Lock the real mouse so noone hears it
mouse.grab()


class KeyEventProcessor:
    def process_key_event(self, key_event):
        pass


class AcmeProcessor(KeyEventProcessor):
    def process_key_event(self, key_event):
        state = key_event.keystate
        virtual_mouse.write(ecodes.EV_KEY, ecodes.BTN_MIDDLE, state)


class XxxProcessor(KeyEventProcessor):
    def process_key_event(self, key_event):
        print(key_event.keycode)


processors = {"acme": AcmeProcessor(), "xxx": XxxProcessor()}


# Read the mouse loop and write events to the virtual mouse conditionally
async def handle_mouse():
    async for event in mouse.async_read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            print(key_event.keycode)
            if key_event.keycode == "BTN_SIDE" or key_event.keycode == "BTN_EXTRA":
                processors["acme"].process_key_event(key_event)
                continue
            else:
                virtual_mouse.write_event(event)
        else:
            virtual_mouse.write_event(event)

asyncio.ensure_future(handle_mouse())

event_loop = asyncio.get_event_loop()
event_loop.run_forever()

