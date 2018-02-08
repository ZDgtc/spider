#coding: utf-8
import sqlite3


class DataOutput(object):
    def __init__(self):
        self.cx = sqlite3.connect('MTime.db')
        self.create_table('MTime')
        self.datas = []

    def create_table(self, table_name):
        values = '''
        id integer primary key,
        MovieId integer,
        MovieTitle varchar(40) NOT NULL,
        RatingFinal REAL NOT NULL DEFAULT 0.0,
        ROtherFinal REAL NOT NULL DEFAULT 0.0,
        RPictureFinal REAL NOT NULL DEFAULT 0.0,
        RDirectorFinal REAL NOT NULL DEFAULT 0.0,
        RStoryFinal REAL NOT NULL DEFAULT 0.0,
        Usercount integer NOT NULL DEFAULT 0,
        AttitudeCount integer NOT NULL DEFAULT 0,
        TotalBoxOffice varchar(20) NOT NULL,
        TodayBoxOffice varchar(20) NOT NULL,
        Rank integer NOT NULL DEFAULT 0,
        ShowDays integer NOT NULL DEFAULT 0,
        releaseType integer NOT NULL
        '''
        self.cx.execute('CREATE TABLE IF NOT EXISTS %s( %s )' % (table_name, values))

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas) > 10:
            self.output_db('MTime')

    def output_db(self):
        pass