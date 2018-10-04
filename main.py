# PackMan (https://github.com/derco0n/PackMan):

# Main Module

import sys
import core.boardman
import core.config
import core.database_mysql


def start():
    """ Main entry point """
    print("Welcome to PackMan. You are running Python-version: "+sys.version)

    # Get current config
    myconf = core.config.Config("/etc/packman/packman.conf")

    # Print current config
    myconf.printconfig()

    # Board-Manager-Examples:
    # Initialize Board ID 0 (iterate for Piface-Stack [Check Jumpers JP1 and JP2]) in Inputmode=Button with 8 Inputs
    # bman = core.boardman.Boardmanager(0, "button", 8)

    # Initialize Board ID 0 (iterate for Piface-Stack [Check Jumpers JP1 and JP2]) in Inputmode=Switch with 8 Inputs
    # bman=core.boardman.Boardmanager(0, "switch", 8)

    # Initialize Board ID 1 (iterate for Piface-Stack [Check Jumpers JP1 and JP2]) in Inputmode=Switch with 6 Inputs
    # bman=core.boardman.Boardmanager(1, "switch", 6)
    # etc. ...

    # Initialize one Boardmanager per Board...
    count=0
    boardmanagers=[]
    while count < myconf.pifaceboards.boardcount:
        boardmanagers.append(core.boardman.Boardmanager(count,
                                                        myconf.pifaceboards.inputmode,
                                                        myconf.pifaceboards.inputsperboard)
                             )
        count = count+1
    print("Boardmanager(s) initialized...")

    # Establish-Database-connection
    mydb = core.database_mysql.db_mysql(
        myconf.mysql.server,
        myconf.mysql.user,
        myconf.mysql.password,
        myconf.mysql.db,
        myconf.mysql.inputstable
    )

    # TODO: Do some useful stuff. Bringing it all together...

    # Test Database
    mydb.write_input_state(2, 0)  # Set Pin 2 to LOW
    print(str(mydb.read_input_state(2)))
    mydb.write_input_state(2, 1)  # Set Pin 2 to HIGH
    print(str(mydb.read_input_state(2)))

    print("Ready...")







