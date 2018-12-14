# PackMan (https://github.com/derco0n/PackMan):
# Database-Connector for MySQL/MariaDB

import mysql.connector

class db_mysql:
    def __init__(self, hostname, username, password, database, statestable, logstable, acommit=True):
        self.host = hostname
        self.user = username
        self.password = password
        self.database = database
        self.statestable = statestable
        self.logstable = logstable
        self.acommit = acommit
        self.establish_connection()  # Establish SQL-Connection

    def establish_connection(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            db=self.database,
            autocommit=self.acommit  # Autocommit statements when their transactions complete
        )
        self.statestable = self.statestable
        self.logstable = self.logstable
        # self.connection.autocommit = True  # Autocommit statements when their transactions complete
        # print(self.connection)  # DEBUG

    def assure_sql_connection(self):
        # Checks if the connection is still alive and reconnects if not
        if not self.connection.is_connected():
            # Connection ist not established or lost in the meantime
            self.establish_connection()

    def execute_statement(self, statement):
        # Executes an SQL-Statement
        self.assure_sql_connection()
        mycursor = self.connection.cursor()
        mycursor.execute(statement)
        return mycursor

    def getresult(self, cursor):
        # Gets the result from a SQL-Cursor returned by a fired statement
        return cursor.fetchall()

    def read_input_state(self, inputID):
        # Reads the current state of a given Input from Database
        statement = "SELECT state FROM "+self.statestable+" WHERE inputID="+str(inputID)+" LIMIT 1"
        res = self.getresult(self.execute_statement(statement))
        state=0
        for row in res:
            state = int(row[0])  # Get the binary state-value from res and convert it to int
        return state

    def check_input_exists_in_db(self, inputID):
        # Checks if a given inputID exists in Database
        statement = "SELECT EXISTS(SELECT inputID FROM " + self.statestable + " WHERE InputID=" + str(inputID) + ")"
        res = self.getresult(self.execute_statement(statement))
        exists = 0
        for row in res:
            exists = int(row[0])  # Get the binary state-value from res and convert it to int
        return exists

    def write_input_state(self, inputID, state):
        # Writes a state to the Database
        # First Check if inputID exists in DB before setting its value...
        if self.check_input_exists_in_db(inputID) == 1:
            # If inputID was found in Database...
            # Check if new state is 1 or 0 and nothing else
            if state == 1 or state == 0:
                # ... then update the value for the Input
                statement = "UPDATE " + self.statestable + " set state=" + str(state) + " WHERE inputID=" + str(inputID)
                res = self.execute_statement(statement)
                return True
            return False
        else:
            # Input not found in Database
            # Check if new state is 1 or 0 and nothing else
            # And add Input if not exist...
            if state == 1 or state == 0:
                statement = "INSERT INTO " + self.statestable + " (inputID, state, description) VALUES (" + \
                            str(inputID) + ", " + str(state) + \
                            ", \"Added automatically by PackMan-Sensor\")"
                res = self.execute_statement(statement)
                return True
            return False

    def write_log(self, eventID, extra=""):
        # Writes an event-log-entry to the database
        # Possible Events are:
        # +-------+--------------------------------+------------------------------------------------------------------------+
        # | ev_id | eventtext                      | description                                                            |
        # +-------+--------------------------------+------------------------------------------------------------------------+
        # |     1 | Input switched to HIGH         | A Digital-Input switched to HIGH signals an inbound Package            |
        # |     2 | Input switched to LOW          | A Digital-Input switched to LOW signals a Package fetched by someone   |
        # |     3 | Input toggled                  | A Digital-Input had been triggered in button-mode                      |
        # |     4 | E-Mail -Package inbound- sent  | An E-Mail notifying an inbound Package has been sent                   |
        # |     5 | E-Mail -Package fetched - sent | An E-Mail notifying an fetched Package has been sent                   |
        # |     6 | packMan-Sensor started         | The sensor-software on the Raspberry-Pi has been started               |
        # |     7 | Frontend accessed              | The Webfrontend was accessed. Log-Extra-info may contain the IP-Adress |
        # +-------+--------------------------------+------------------------------------------------------------------------+
        if eventID >= 1 and eventID <= 6:
            if extra == "":
                statement = "INSERT INTO " + self.logstable + "(ev_id) VALUES ("+str(eventID) + ")"
            else:
                statement = "INSERT INTO " + self.logstable + "(ev_id, extra_info) VALUES (" + str(eventID) + ", \"" + extra + "\")"
            self.execute_statement(statement)
            return True
        return False
