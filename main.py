import sys
import core.boardman


def start():
    """ Main entry point """
    print("Welcome to PackMan. You are running Python-version: "+sys.version)
    # bman = core.boardman.Boardmanager(0, "button", 8)  # Initialize Board with ID 0 (iterate for Piface-Stack [Check Jumpers JP1 and JP2]) in Inputmode=Button with 8 Inputs
    bman=core.boardman.Boardmanager(0, "switch", 8)  # Initialize Board with ID 0 (iterate for Piface-Stack [Check Jumpers JP1 and JP2]) in Inputmode=Switch with 8 Inputs




