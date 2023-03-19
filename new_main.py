from appointment import Appointment
from datetime import datetime, timedelta
import calendar
import sqlite3
import json
import csv

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

connection = sqlite3.connect("appointments.db")
connection.row_factory = dict_factory

cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS appointments (
                    first_name TEXT,
                    second_name TEXT, 
                    date TEXT, 
                    duration TEXT, 
                    end TEXT, 
                    status TEXT
                    )""")

"""
1. User login
"""
first_name = input("What is your first name?: ")
second_name = input("What is your second name?: ")

"""
Main Menu
"""
while True:
    action = input("""What would you like to do?
                   1. Book a reservation
                   2. Cancel a reservation
                   3. Print schedule
                   4. Save schedule to file
                   5. Exit
                   Please select an option (1-5): """)
    """
    1. Book a reservation
    """
    if action == "1":
        new_instance = Appointment()
        new_instance.first_name = first_name
        new_instance.second_name = second_name
        year = input("Select year of reservation (YYYY): ")
        month = input("Select month of reservation (1-12): ")
        days = calendar.monthrange(int(year), int(month))
        """tu zrobić test na poprawność daty, dzień nie może być większy niż ilość dni w miesiącu,
        czyli days >= day"""
        day = input(f"Select day of reservation (1-{days[1]}): ")
        hour = input("Select hour of reservation (HH:MM): ")
        new_instance.date = "{}-{}-{}-{}".format(year, month, day, hour)
        duration = input("Select duration of reservation in minutes (30,60,90): ")
        new_instance.duration = duration
        new_instance.end = datetime.strptime(new_instance.date, "%Y-%m-%d-%H:%M") + timedelta(minutes=int(duration))
        """
        Najpierw szukamy czy w bazie danych jest już taka rezerwacja
        """
        cursor.execute("SELECT * FROM appointments "
                       f"WHERE date='{new_instance.date}'")
        data = cursor.fetchall()
        difference = datetime.strptime(datetime.now().strftime("%Y-%m-%d-%H:%M"), "%Y-%m-%d-%H:%M") - datetime.strptime(new_instance.date, "%Y-%m-%d-%H:%M")
        print(difference)
        if len(data) > 0:
            print("Sorry, this date is already taken")
            continue
        else:
            new_instance.status = "confirmed"
            cursor.execute("INSERT INTO appointments VALUES (:first_name, :second_name, :date, :duration, :end, :status)",
                           {'first_name': new_instance.first_name,
                            'second_name': new_instance.second_name,
                            'date': new_instance.date,
                            'duration': new_instance.duration,
                            'end': new_instance.end,
                            'status': new_instance.status})
            connection.commit()
            print(f"Your reservation is confirmed for {new_instance.date} to {new_instance.end}")
            print(new_instance.__dict__)
            continue
    if action == "2":
        cursor.execute("SELECT * FROM appointments "
                       f"WHERE first_name='{first_name}' "
                       f"AND second_name='{second_name}'")
        data = cursor.fetchall()
        for count,row in enumerate(data):
            print(f"{count}. {row['first_name']} {row['second_name']} {row['date']} - {row['end']}")
        choice = input("Select reservation to cancel: ")
        to_delete = data[int(choice)]
        cursor.execute(f"DELETE FROM appointments "
                       f"WHERE first_name='{to_delete['first_name']}'"
                       f"AND second_name='{to_delete['second_name']}'"
                       f"AND date='{to_delete['date']}'")
        connection.commit()
        continue
    if action == "3":
        cursor.execute("SELECT * FROM appointments "
                       f"WHERE first_name='{first_name}'"
                       f"AND second_name='{second_name}'")
        data = cursor.fetchall()
        for count,row in enumerate(data):
            print(f"{count}. {row['first_name']} {row['second_name']} {row['date']} - {row['end']}")
        continue
    if action == "4":
        file_type = input("Select file type (json/csv): ")
        if file_type == "json":
            cursor.execute("SELECT * FROM appointments "
                           f"WHERE first_name='{first_name}' "
                           f"AND second_name='{second_name}'")
            data = cursor.fetchall()
            to_json = json.dumps(data)
            export_json = open("appointments.json", "w")
            export_json.write(to_json)
            export_json.close()
            continue
        if file_type == "csv":
            cursor.execute("SELECT * FROM appointments "
                           f"WHERE first_name='{first_name}' "
                           f"AND second_name='{second_name}'")
            data = cursor.fetchall()
            headers = ["first_name", "second_name", "date", "duration", "end", "status"]
            with open("appointments.csv", "w") as export_csv:
                writer = csv.DictWriter(export_csv, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
                export_csv.close()
            continue
    if action == "5":
        break

connection.close()