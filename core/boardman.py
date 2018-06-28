import pifacedigitalio
import threading
# import pifacedigital_emulator


class Boardmanager:


    def buttonpressed(self, event):
        # Callback-method for button ... pressed
        event.chip.leds[event.pin_num].toggle()
        # print(event)  # DEBUG

    def switchon(self, event):
        # Callback-method for switch ... turned on
        event.chip.leds[event.pin_num].turn_on()
        # print(event)  # DEBUG

    def switchoff(self, event):
        # Callback-method for switch ... turned on
        event.chip.leds[event.pin_num].turn_off()
        # print(event)  # DEBUG

    def __init__(self, bid, inputmode="switch", inputcount=8):
        self.boardid = bid  # Defines the SPI-Bus Number of the PiFace-Board
        # Determine if Input is a button or a switch (default)
        if inputmode == "switch" or inputmode == "button":
            self.inputmode=inputmode
        else:
            self.inputmode="switch"

        self.maxinput= inputcount-1  # Set highest input-Nr. input numbers starting at index 0. therefore highest input-number ist -1
        try:
            self.pfd = pifacedigitalio.PiFaceDigital(self.boardid)  # Create a new PifaceDigital Object
        except:
            print("Board with ID=" + bid + " not found. Please check your numbering and Jumpers on your board!")
            return

        # Initialize input-Event-Listener
        self.eventlistener = pifacedigitalio.InputEventListener(chip=self.pfd)  # New Listenerobject

        # register Eventlistener for each input
        input = 0  # Current input number
        while input <= self.maxinput:  # Iterate through all possible inputs
            try:
                if self.inputmode == "button":
                    # Button-mode
                    self.eventlistener.register(input, pifacedigitalio.IODIR_FALLING_EDGE, self.buttonpressed)  # Listen for Inputevents on button >>input<<
                else:
                    # Switch-Mode
                    self.eventlistener.register(input, pifacedigitalio.IODIR_ON, self.switchon)  # Listen for Inputevents for Switch Enable at >>input<<
                    self.eventlistener.register(input, pifacedigitalio.IODIR_OFF, self.switchoff)  # Listen for Inputevents for Switch Disable at >>input<<
            except:
                print("Listener for input #"+input+" could not be registered!")
            input = input + 1  # got to next input

        self.activateListener()  # Enable Listener

    def activateListener(self):
        self.eventlistener.activate()

    def deactivateListener(self):
        self.eventlistener.deactivate()
