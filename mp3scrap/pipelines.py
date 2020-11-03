# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pyodbc
from .items import Mp3SongsItem,Mp3MovieItem

class Mp3ScrapPipeline:
    def __init__(self):
        self.create_Conn()

    def create_Conn(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=IDEA-PC;DATABASE=SONGSMP3;UID=sa;PWD=')
        self.curr = self.conn.cursor()

    def process_Movie(self, item, spider):
        self.curr.execute("""insert into BOLLYWOOD_MOVIE_DETAILS values (?,?,?,?,?,?,?,?)""", (
            item['name'],
            item['year'],
            item['url'],
            item['Stars'],
            item['Director'],
            item['M_Director'],
            item['Composer'],
            item['Singer']

        ))
        self.conn.commit()
        return item

    def process_Song(self, item, spider):

        id=self.curr.execute(""" select Movie_ID from BOLLYWOOD_MOVIE_DETAILS where Name=? """,(item['Mov_Name']))
        self.curr.execute("""insert into BOLLYWOOD_SONGS_DETAILS values (?,?,?,?,?)""", (
            id.fetchval(),
            item['Title'],
            item['Artist'],
            item['url'],
            item['Size']
        ))

        self.conn.commit()
        return item

    def process_item(self, item, spider):
        if isinstance(item,Mp3MovieItem ):
            self.process_Movie(item,spider)
        if isinstance(item, Mp3SongsItem):
            self.process_Song(item, spider)
