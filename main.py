# PackMan (https://github.com/derco0n/PackMan):

# Main Module

import sys
import os
import core.boardman
import core.config
import core.database_mysql
import threading
import signal
import time

VERSION = "0.13"
DEFAULTCONFIG = "/etc/packman/packman.conf"


class Start:
    def __init__(self, configfile=DEFAULTCONFIG):
        print("PackMan starting...")
        self.shouldexit = False
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        self.configfile = configfile

        self.start()

    def signal_handler(self, signum, frame):
        # print('Aborting...')
        self.shouldexit = True

    def shutdown(self):

        if self.getalltimer is not None:
            print("Stopping Timer")
            self.getalltimer.stop()

        # Stop Event-Listeners
        print("Stopping Input-Event-Listeners...")
        for bm in self.boardmanagers:
            # deregister Events
            if bm.listenersactive:
                bm.events.on_pinup -= self.handle_pinon
                bm.events.on_pindown -= self.handle_pinoff
                bm.events.on_pintoggle -= self.handle_pintoggle

                # Stop Listener-Thread
                bm.stop()
                print("Board: " + str(bm.boardid) + " done.")

        # Close Database connection
        if self.mydb.connection.is_connected():
            print("Closing DB-connection...")
            self.mydb.connection.disconnect()
        print("Bye")
        os._exit(0)  # The hard way to exit a programm, as it does not cleanup something

    def handle_pintoggle(self, boardid, linearinput):  # Eventhandler (for Boardman-Event...)
        self.mydb.write_log(3, "Board: " + str(boardid) + ", Pin: " + str(linearinput))
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
        self.mydb.write_log(2, "Board: " + str(boardid) + ", Pin: " + str(linearinput))
        self.mydb.write_input_state(linearinput, 0)
        # print(event) # DEBUG

    def initialize_inputstates(self):
        # Gets current Input-States and sets them in Database
        # This should be triggered at startup and eventually in intervalls (to make sure you dont miss a state change)

        # (Re-)trigger this Method every 5 Minutes (300 seconds) with a timer Event
        self.getalltimer = threading.Timer(300.0, self.initialize_inputstates).start()  # comment this out if you dont want to pull inputs in intervalls

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

    def start(self):
        """ Main entry point """

        print("Welcome to PackMan (Version: " + VERSION + "). You are running Python-version: "+sys.version)

        # Get current config
        self.myconf = core.config.Config(self.configfile)

        if not self.myconf.hasallboardvalues:
            print("Not all board-value-definitions found. Please check your config-file. Aborting")
            return 1

        if not self.myconf.hasallsqlvalues:
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

        self.mydb.write_log(6, "Version: " + VERSION + ", Config: " + self.configfile)  # Write Log-Entry: Sensor started

        # Initialize one Boardmanager per Board...
        boardcount = 0
        self.boardmanagers = []
        while boardcount < self.myconf.pifaceboards.boardcount:
            self.boardmanagers.append(core.boardman.Boardmanager(boardcount,
                                                                 self.myconf.pifaceboards.inputmode,
                                                                 self.myconf.pifaceboards.inputsperboard))
            # Increment counter

            boardcount = boardcount + 1
        print("Boardmanager(s) initialized...")

        self.initialize_inputstates()  # Initalize Input-states at startup



        # Initialize Input-Event-listeners (to recognize Input-changes by Interrupt)
        for bm in self.boardmanagers:
            # register Events
            bm.events.on_pinup += self.handle_pinon
            bm.events.on_pindown += self.handle_pinoff
            bm.events.on_pintoggle += self.handle_pintoggle

            # Start Listener-Thread
            bm.run()

        print("Ready...")

        while self.shouldexit == False:
           time.sleep(1)

        self.shutdown()






