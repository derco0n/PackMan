# PackMan (https://github.com/derco0n/PackMan):
# Config-component

# Reads a config from a file
# Configfile must look like this:
# [mysql]
# server=servername.fqdn.tld
# user=databaseuser
# pass=password
# database=database_to_use
# inputstable=tablename_used_for_digital-input-states
#
# [pifaceboards]
# boardcount=1
# inputsperboard=8
# inputmode=switch

import configparser
import core.settings_mysql
import core.settings_pfb


class Config:
    def __init__(self, configfile="/etc/packman/packman.conf"):
        self.configfile=configfile
        self.mysql = core.settings_mysql.settings_mysql()
        self.pifaceboards = core.settings_pfb.settings_pifaceboards()
        self.readconfig()

    def printconfig(self):
        # Prints out current values, which are read from configfile
        print("Config was read from: " + self.configfile)
        print("")
        print("MySQL-Server: " + self.mysql.server)
        print("MySQL-User: " + self.mysql.user)
        # print("MySQL-Password: "+ self.mysql.password)  # DEBUG (use with caution!)
        print("MySQL-DB: " + self.mysql.db)
        print("PiFace-Boardcount: " + str(self.pifaceboards.boardcount))
        print("PiFace-Inputcount: " + str(self.pifaceboards.inputsperboard))
        print("PiFace-Inputmode: " + self.pifaceboards.inputmode)

    def readconfig(self):
        # Reads settings from a configfile specified in constructor...

        config = configparser.ConfigParser()
        config.read(self.configfile)

        # Section mysql
        if 'mysql' in config:
            # Config contains section "[mysql]"
            try:
                self.mysql.server = config.get('mysql', 'server')
            except:
                print("Did not found value for server in "+self.configfile)

            try:
                self.mysql.user = config.get('mysql', 'user')
            except:
                print("Did not found value for user in "+self.configfile)

            try:
                self.mysql.password = config.get('mysql', 'pass')
            except:
                print("Did not found value for pass in " + self.configfile)

            try:
                self.mysql.db = config.get('mysql', 'database')
            except:
                print("Did not found value for database in " + self.configfile)

            try:
                self.mysql.inputstable = config.get('mysql', 'inputstable')
            except:
                print("Did not found value for inputstable in " + self.configfile)

        # Section pifaceboards
        if 'pifaceboards' in config:
            # Config contains section "[pifaceboards]"
            try:
                self.pifaceboards.boardcount = config.getint('pifaceboards', 'boardcount')
            except:
                print("Did not found value for boardcount in " + self.configfile)

            try:
                self.pifaceboards.inputsperboard = config.getint('pifaceboards', 'inputsperboard')
            except:
                print("Did not found value for inputsperboard in " + self.configfile)

            try:
                self.pifaceboards.inputmode = config.get('pifaceboards', 'inputmode')
            except:
                print("Did not found value for inputmode in " + self.configfile)

