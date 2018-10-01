import pifacedigitalio
# import pifacedigital_emulator


class Boardmanager:
    def __init__(self, bid):
        self.boardid = bid  # Defines the SPI-Bus Number of the PiFace-Board
        try:
            self.pfd = pifacedigitalio.PiFaceDigital(self.boardid)  # Create a new PifaceDigital Object
            # Initialize input-Event-Listener
            self.eventlistener = pifacedigitalio.InputEventListener(chip=pifacedigitalio.PiFaceDigital)
            self.eventlistener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, self.toggle_led0)
        except:
            print("Board with ID="+bid+" not found. Please check your numbering and Jumpers on your board!")

    def toggle_led0(event):
        event.chip.leds[0].toggle()

    def dout_on(self, nr):
        if nr >= 0 and nr <= 7:
            self.pfd.leds[nr].turn_on()
        else:
            print("Invalid Output-value!")

    def dout_off(self, nr):
        if nr >= 0 and nr <= 7:
            self.pfd.leds[nr].turn_off()
        else:
            print("Invalid Output-value!")

    def activateListener(self):
        self.eventlistener.activate()

    def deactivateListener(self):
        self.eventlistener.deactivate()
