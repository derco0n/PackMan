# PackMan (https://github.com/derco0n/PackMan):

# Main Module

import sys
import core.boardman
import core.config
import core.database_mysql

VERSION="0.1"
DEFAULTCONFIG="/etc/packman/packman.conf"

def start():
    """ Main entry point """

    configfile = DEFAULTCONFIG


    print("Welcome to PackMan. You are running Python-version: "+sys.version)

    # Get current config
    myconf = core.config.Config(configfile)

    if myconf.hasallboardvalues == False:
        print("Not all board-value-definitions found. Please check your config-file. Aborting")
        return 1

    if myconf.hasallsqlvalues == False:
        print("Not all Database-value-definitions found. Please check your config-file. Aborting")
        return 2


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

    # Establish-Database-connection
    mydb = core.database_mysql.db_mysql(
        myconf.mysql.server,
        myconf.mysql.user,
        myconf.mysql.password,
        myconf.mysql.db,
        myconf.mysql.inputstable,
        myconf.mysql.logstable
    )

    mydb.write_log(5, "Version: " + VERSION + ", Config: " + configfile)  # Write Log-Entry: Sensor started

    # Initialize one Boardmanager per Board...
    boardcount = 0
    boardmanagers = []
    while boardcount < myconf.pifaceboards.boardcount:
        boardmanagers.append(core.boardman.Boardmanager(boardcount,
                                                        mydb,
                                                        myconf.pifaceboards.inputmode,
                                                        myconf.pifaceboards.inputsperboard)
                             )

        boardcount = boardcount + 1
    print("Boardmanager(s) initialized...")

    # TODO: Fetch Events raised from ech boardman here, so wen can calculate linear-pin-number and talk to database in main


    print("Ready...")







