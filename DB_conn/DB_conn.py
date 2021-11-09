from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .DB_tables import Base, User, Record
import datetime


class DBConnection:
    __url = ""

    def __init__(self):
        self.engine = create_engine(self.__url, echo=True)
        self.session = sessionmaker(bind=self.engine)
        self.s = self.session()

    def add_user(self, username, us_name, us_sname):
        user = User(username=username, us_name=us_name, us_sname=us_sname)
        self.s.add(user)
        self.s.commit()

    def add_record(self, rec_text, un):
        u_id = [row.id_user for row in self.s.query(User).filter(User.username == un)]
        rec = Record(rec_date=datetime.datetime.now(), rec_text=rec_text, user_id=u_id[0])
        self.s.add(rec)
        self.s.commit()

    def get_user(self, un):
        result = self.s.query(User).filter(User.username == un)
        rows = []
        for row in result:
            rows.append({"id_user": row.id_user,
                         "username": row.username,
                         "us_name": row.us_name,
                         "us_sname": row.us_sname})

    def get_record(self, un):
        u_id = [row.id_user for row in self.s.query(User).filter(User.username == un)]
        result = self.s.query(Record).filter(Record.user_id == u_id[0])
        recs = []
        for row in result:
            recs.append({"date": row.rec_date,
                         "text": row.rec_text})

        return recs


if __name__ == "__main__":
    con = DBConnection()
    # con.add_user("Vasya777", "Vasya", "Pupkin")
    # con.add_record("Не опоздать к врачу", user_id=1)
    print(con.get_record("Vasya777"))

