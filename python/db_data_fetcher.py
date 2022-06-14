import db_connect as db

from datetime import datetime


class DB_Data_Fetcher:
    def __init__(self):
        self.days = None
        self.jobtypes = None
        self.users = None
        self.helpers = None
        self.jobs = None
        print(db.fetch_days())
        print(50*"-")
        print(db.fetch_jobtypes())
        print(50*"-")
        print(db.fetch_jobs())
        print(50*"-")
        print(db.fetch_users())
        print(50*"-")
        print(db.fetch_helpers())
        print(50*"-")

if __name__ == "__main__":
    db_Fetcher = DB_Data_Fetcher()
