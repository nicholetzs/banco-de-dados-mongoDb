import mysql.connector


class MySql:
    def __init__(self, config):
        self.config = config

    def get_connection(self):
        return mysql.connector.connect(**self.config)
