# This is an example how to listen to input-events on a PiFace-Board...
# This file is just for testing purpose and not used in productive

import pifacedigitalio


def button0pressed(event):
    event.chip.leds[0].toggle()
    print(event)


def button1pressed(event):
    event.chip.leds[1].toggle()
    print(event)


pifacedigital = pifacedigitalio.PiFaceDigital(0)
listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
listener.register(0, pifacedigitalio.IODIR_RISING_EDGE, button0pressed)
listener.register(1, pifacedigitalio.IODIR_RISING_EDGE, button1pressed)
listener.activate()

