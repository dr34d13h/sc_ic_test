from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, and_
from datetime import datetime


engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3305/pyloungedb", echo=True)
meta = MetaData(engine)


Events = Table('Events', meta, autoload=True)


class Event():
    def __init__(self, author_id, event_name, event_header, event_description, event_media, event_date, event_datetime):
        self.author_id = author_id
        self.event_name = event_name
        self.event_header = event_header
        self.event_description = event_description
        self.event_media = event_media
        self.event_date = event_date
        self.event_datetime = event_datetime

    def __repr__(self):
        return "<Event('%s', '%s', '%s', '%s', '%s', '%s', '%s'>" % (self.author_id, self.event_name, self.event_header, self.event_description, self.event_media, self.event_date, self.event_datetime)


mapper(Event, Events)


async def add_event(data, author_id):
    ins_event = Event(
        author_id = int(author_id),
        event_name = str(data['event_name']),
        event_header = str(data['event_header']),
        event_description = str(data['event_description']),
        event_media = str(data['event_media'][0]) + '#' + str(data['event_media'][1]),
        event_date = str(data['event_date']),
        event_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.add(ins_event)
    session.commit()


async def get_events():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    all_events = []
    for event in session.query(Event):
        all_events.append(event)    
    return all_events


async def get_event(name):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    event = session.query(Event).filter_by(event_name = name).one()
    return event


async def del_event(all_events):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.query(Event).filter_by(event_name = all_events.event_name).delete()
    session.commit()

