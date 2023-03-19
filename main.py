from appointment import Appointment
from datetime import datetime, timedelta
import calendar
import sqlite3
import json
import csv
today = datetime.now().strftime("%Y-%m-%d-%H:%M")
print(today)
print(type(today))
#
# def dict_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#     return d
#
# connection = sqlite3.connect("appointments.db")
# connection.row_factory = dict_factory
#
# cursor = connection.cursor()
# cursor.execute("""CREATE TABLE IF NOT EXISTS appointments (
#                     first_name TEXT,
#                     second_name TEXT,
#                     date TEXT,
#                     duration TEXT,
#                     end TEXT,
#                     status TEXT
#                     )""")
#
#
# """
# 1. Name input
# """
# Appointment.first_name = input("What is your first name?: ")
# Appointment.second_name = input("What is your second name?: ")
# """
# 2. Reservation or cancellation
# """
# action = input("Would you like to book a reservation or cancel a reservation? (b/c): ")
# if action == "b":
#     """
#     3R. Date input
#     """
#     new_instance = Appointment()
#     year = input("Select year of reservation (YYYY): ")
#     month = input("Select month of reservation (1-12): ")
#     days = calendar.monthrange(int(year), int(month))
#     """tu zrobić test na poprawność daty, dzień nie może być większy niż ilość dni w miesiącu,
#     czyli days >= day"""
#     day = input("Select day of reservation (1-31): ")
#     hour = input("Select hour of reservation (HH:MM): ")
#     new_instance.date = "{}-{}-{}-{}".format(year, month, day, hour)
#     duration = input("Select duration of reservation in minutes (30,60,90): ")
#     new_instance.duration = duration
#     new_instance.end = datetime.strptime(new_instance.date, "%Y-%m-%d-%H:%M") + timedelta(minutes=int(duration))
#     new_instance.status = "confirmed"
#     cursor.execute("INSERT INTO appointments VALUES (:first_name, :second_name, :date, :duration, :end, :status)",
#                    {'first_name':new_instance.first_name,
#                     'second_name':new_instance.second_name,
#                     'date':new_instance.date,
#                     'duration':new_instance.duration,
#                     'end':new_instance.end,
#                     'status':new_instance.status})
#     connection.commit()
#     print(f"Your reservation is confirmed for {new_instance.date} to {new_instance.end}")
# cursor.execute("SELECT * FROM appointments WHERE first_name='Jan'")
# data = cursor.fetchall()
# my_json = json.dumps(data)
# export_json = open("export.json", "w")
# export_json.write(my_json)
# export_json.close()
# headers = ["first_name", "second_name", "date", "duration", "end", "status"]
# export_csv = open("export.csv", "w")
# with open("export.csv", "w") as c:
#     writer = csv.DictWriter(c, fieldnames=headers)
#     writer.writeheader()
#     writer.writerows(data)
#     c.close()
#
# connection.close()
#
