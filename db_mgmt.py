import mysql.connector
import datetime

class dbManage():
    def __init__(self, v1, v2, v3, v4):
        try:
            self.mydb = mysql.connector.connect(
                host=v1,
                user=v2,
                password=v3,
                database=v4
            )
        except Exception as e:
            print("Failed to initialise dbManage\nError message:", e)

    def insert_power_used(self, watts):
        try:
            cursor = self.mydb.cursor()

            current_date_time = datetime.datetime.now()

            values = watts, current_date_time

            cursor.execute("INSERT INTO power_used (watts, added) VALUES (%s, %s)", values)

            self.mydb.commit()

        except Exception as e:
            self.mydb.rollback()

            print("Failed to insert power_used\nError message:", e)


