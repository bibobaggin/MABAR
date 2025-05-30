# utils.py
import csv, os

USER_DB = "users.csv"

def get_display_name(username):
    if not os.path.exists(USER_DB):
        return username
    with open(USER_DB, newline="") as f:
        for row in csv.reader(f):
            if row and row[0]==username:
                return row[2]
    return username
