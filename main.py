import sys
import core.boardman
import _thread
import pifacedigitalio  # DEBUG

def start():
    """ Main entry point """
    print("Welcome to PackMan. You are running Python-version: "+sys.version)
    bman=core.boardman.Boardmanager(0)  # Initialize Board with ID 0
    # For Use with PiFaceStack (Check Jumpers JP1 and JP2)
    # bman=core.boardman.Boardmanager(1)  # Initialize Board with ID 1
    # bman=core.boardman.Boardmanager(2)  # Initialize Board with ID 2
    # bman=core.boardman.Boardmanager(3)  # Initialize Board with ID 3

    # Test
    # mylistener.dout_on(1)
    # mylistener.dout_off(1)
    # Fin-Test

    # Eventlistener starten

    # DEBUG
    # pifacedigital = pifacedigitalio.PiFaceDigital()
    # listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    # listener.register(0, pifacedigitalio.IODIR_RISING_EDGE, print)
    # listener.activate()

    return True