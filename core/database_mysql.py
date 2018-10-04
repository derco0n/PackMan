# PackMan (https://github.com/derco0n/PackMan):
# Database-Connector mysql

import mysql.connector

class db_mysql:
    def __init__(self, hostname, username, password, database, statestable):
        self.connection = mysql.connector.connect(
            host=hostname,
            user=username,
            passwd=password,
            db=database
        )
        self.statestable = statestable

        # print(self.connection)  # DEBUG

    def execute_statement(self, statement):
        # Executes an SQL-Statement
        mycursor = self.connection.cursor()
        mycursor.execute(statement)
        return mycursor

    def getresult(self, cursor):
        return cursor.fetchall()

    def read_input_state(self, inputID):
        # Reads the current state of a given Input from Database
        statement = "SELECT state FROM "+self.statestable+" WHERE inputID="+str(inputID)+" LIMIT 1"
        res = self.getresult(self.execute_statement(statement))
        for row in res:
            state = int(row[0])  # Get the binary state-value from res and convert it to int
        return state

    def write_input_state(self, inputID, state):
        # Writes a state to the Database
        # TODO: May be check if inputID exists in DB before setting its value...
        if state == 1 or state == 0:
            statement = "UPDATE " + self.statestable + " set state=" + str(state) + " WHERE inputID=" + str(inputID)
            res = self.execute_statement(statement)
            return True
        return False

