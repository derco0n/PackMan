# PackMan (https://github.com/derco0n/PackMan):

# Main Module

import sys
import core.boardman
import core.config
import core.database_mysql

VERSION = "0.1"
DEFAULTCONFIG = "/etc/packman/packman.conf"

class start:
    def __init__(self, configfile=DEFAULTCONFIG):
        self.configfile = configfile
        self.start()

    def handle_pintoggle(self, boardid, linearinput):  # Eventhandler (for Boardman-Event...)
        self.mydb.write_log(1, "Board: " + str(boardid) + ", Pin: " + str(linearinput))
        currentstate = self.mydb.read_input_state(linearinput)  # get current state in db

        # Invert current db-state, as pin had been toggled...
        if currentstate == 0:
            self.mydb.write_input_state(linearinput, 1)
        else:
            self.mydb.write_input_state(linearinput, 0)
        # print(event) # DEBUG

    def handle_pinon(self, boardid, linearinput):  # Eventhandler (for Boardman-Event...)
        self.mydb.write_log(1, "Board: " + str(boardid) + ", Pin: " + str(linearinput))
        self.mydb.write_input_state(linearinput, 1)
        # print(event) # DEBUG

    def handle_pinoff(self, boardid, linearinput):  # Eventhandler (for Boardman-Event...)
        self.mydb.write_log(1, "Board: " + str(boardid) + ", Pin: " + str(linearinput))
        self.mydb.write_input_state(linearinput, 0)
        # print(event) # DEBUG

    def start(self):
        """ Main entry point """

        print("Welcome to PackMan. You are running Python-version: "+sys.version)

        # Get current config
        self.myconf = core.config.Config(self.configfile)

        if self.myconf.hasallboardvalues == False:
            print("Not all board-value-definitions found. Please check your config-file. Aborting")
            return 1

        if self.myconf.hasallsqlvalues == False:
            print("Not all Database-value-definitions found. Please check your config-file. Aborting")
            return 2


        # Print current config
        self.myconf.printconfig()

        # Board-Manager-Examples:
        # Initialize Board ID 0 (iterate for Piface-Stack [Check Jumpers JP1 and JP2]) in Inputmode=Button with 8 Inputs
        # bman = core.boardman.Boardmanager(0, "button", 8)

        # Initialize Board ID 0 (iterate for Piface-Stack [Check Jumpers JP1 and JP2]) in Inputmode=Switch with 8 Inputs
        # bman=core.boardman.Boardmanager(0, "switch", 8)

        # Initialize Board ID 1 (iterate for Piface-Stack [Check Jumpers JP1 and JP2]) in Inputmode=Switch with 6 Inputs
        # bman=core.boardman.Boardmanager(1, "switch", 6)
        # etc. ...

        # Establish-Database-connection
        self.mydb = core.database_mysql.db_mysql(
            self.myconf.mysql.server,
            self.myconf.mysql.user,
            self.myconf.mysql.password,
            self.myconf.mysql.db,
            self.myconf.mysql.inputstable,
            self.myconf.mysql.logstable
        )

        self.mydb.write_log(5, "Version: " + VERSION + ", Config: " + self.configfile)  # Write Log-Entry: Sensor started

        # Initialize one Boardmanager per Board...
        boardcount = 0
        self.boardmanagers = []
        while boardcount < self.myconf.pifaceboards.boardcount:
            self.boardmanagers.append(core.boardman.Boardmanager(boardcount,
                                                                 self.myconf.pifaceboards.inputmode,
                                                                 self.myconf.pifaceboards.inputsperboard)
                                 )
            # Increment counter
            boardcount = boardcount + 1
        print("Boardmanager(s) initialized...")


        # Get current Input-States
        allinputstates = {}
        for bm in self.boardmanagers:
            inputs = bm.get_all_input_states()
            # Add the new Key-value-pairs into allinputstates
            allinputstates = dict(allinputstates)
            allinputstates.update(inputs)

        # Initialise DB with current input-states (initial states at startup-time)
        for k in allinputstates.keys():
            val = allinputstates[k]
            self.mydb.write_input_state(k, val)

        # Initialize Input-Event-listeners (to recognize Input-changes by Interrupt)
        for bm in self.boardmanagers:
            # register Events
            bm.events.on_pinup += self.handle_pinon
            bm.events.on_pindown += self.handle_pinoff
            bm.events.on_pintoggle += self.handle_pintoggle

            # Start Listener-Thread
            bm.run()

        print("Ready...")







