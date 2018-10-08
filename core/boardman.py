# PackMan (https://github.com/derco0n/PackMan):

# Boardmanager - Handles a PiFaceDigital-Board in a separate thread

import pifacedigitalio
import threading
from events import Events


class Boardmanager(threading.Thread):

    def buttonpressed(self, event):
        # Callback-method for button ... pressed
        # event.chip.leds[event.pin_num].toggle()  # DEBUG
        linearinput = self.linear_input_number(event.pin_num)  # calculate linear input number
        self.events.on_pintoggle(self.boardid, linearinput)  # Raise Event

    def switchon(self, event):
        # Callback-method for switch ... turned on
        # event.chip.leds[event.pin_num].turn_on()  # DEBUG
        # print(event)  # DEBUG
        linearinput = self.linear_input_number(event.pin_num)  # calculate linear input number
        self.events.on_pinup(self.boardid, linearinput)  # Raise Event

    def switchoff(self, event):
        # Callback-method for switch ... turned on
        # event.chip.leds[event.pin_num].turn_off()  # DEBUG
        # print(event)  # DEBUG
        linearinput = self.linear_input_number(event.pin_num)  # calculate linear input number
        self.events.on_pindown(self.boardid, linearinput)  # Raise Event

    def __init__(self, bid, inputmode="switch", inputcount=8):
        threading.Thread.__init__(self)  # Call Base-class-constructor

        self.events = Events(('on_pinup', 'on_pindown', 'on_pintoggle'))  # declare Events (for handling in Main [or elsewhere])

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
                print("Listener for input #" + input + " could not be registered!")
            input = input + 1  # got to next input

    def get_all_input_states(self):
        # return an array with all current input states
        inputcounter = 0
        inputstates = {}
        while inputcounter <= self.maxinput:
            inputstates[self.linear_input_number(inputcounter)] = self.pfd.input_pins[inputcounter].value
            inputcounter = inputcounter + 1
        return inputstates

    def run(self):
        self.activateListener()  # Enable Listener

    def stop(self):
        self.deactivateListener()  # Disable Listener

    def activateListener(self):
        self.eventlistener.activate()

    def deactivateListener(self):
        try:
            self.eventlistener.deactivate()
        except:
            print("Eventlistener aleready inactive.")


    def linear_input_number(self, inputnumber):
        # returns a linear number over all Inputs
        # Board 0, Input 0 = 0
        # Board 1, Input 0 = 8
        # Board 2, Input 2 = 18 ...
        if inputnumber > self.maxinput:
            # Impossible. inputnumber must be smaller than inputsperboard
            return inputnumber  # TODO: Verify this has no negative side effects
        else:
            linearnumber = self.boardid * self.maxinput + inputnumber  # TODO: Verify this calculation is correct
            return linearnumber

