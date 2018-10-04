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
        mycursor = self.connection.cursor()
        mycursor.execute(statement)
        return mycursor

    def read_input_state(self, inputID):
        statement = "SELECT state FROM "+self.statestable+" WHERE inputID="+str(inputID)+" LIMIT 1"
        res = self.execute_statement(statement)
        state = res  # TODO: Get the binary state-value from res...
        return state