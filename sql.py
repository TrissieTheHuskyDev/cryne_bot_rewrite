from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, query
from sqlite3 import IntegrityError

SQL_Base = declarative_base()

class Server(SQL_Base):
    __tablename__ = "Server"

    sid = Column('sid', Integer, primary_key=True)
    dsid = Column('dsid', Integer, nullable=False, unique=True)
    sname = Column('sname', String, nullable=False)

class ServerSettings(SQL_Base):
    __tablename__ = "ServerSetting"

    setid = Column('setid', Integer, primary_key=True)
    sid = Column('sid', Integer, nullable=False, unique=True)

    logchid = Column('logchid', Integer, nullable=False)
    botcchid = Column('botcchid', Integer, nullable=False)
    remoj = Column('remoj', String, nullable=False)
    rcount = Column('rcount', Integer, nullable=False)
    belvchid = Column('belvchid', Integer, nullable=False)
    banmsgchid = Column('banmsgchid', Integer, nullable=False)
    leavemsgchid = Column('leavemsgchid', Integer, nullable=False)
    kickmsgchid = Column('kickmsgchid', Integer, nullable=False)
    rcmsgchid = Column('rcmsgchid', Integer, nullable=False)
    adminrole = Column('adminrole', String, nullable=False)
    roleonjoin = Column('roleonjoin', String, nullable=False)
    rssurl = Column('rssurl', String, nullable=False)

engine = create_engine('sqlite:///servers.db', echo=True)
SQL_Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def create_server(sname, dsid):
    session = Session()
    server = Server()

    server.sname = sname
    server.dsid = dsid

    session.add(server)
    session.commit()
    session.close()

def create_ssettings(sid ,logchid ,botcchid , remoj , rcount , belvchid ,banmsgchid ,leavemsgchid ,kickmsgchid
                     ,rcmsgchid ,adminrole ,roleonjoin ,rssurl):
    session = Session()
    ssettings = ServerSettings()

    ssettings.sid = sid
    ssettings.logchid = logchid
    ssettings.botcchid = botcchid
    ssettings.remoj = remoj
    ssettings.rcount = rcount
    ssettings.belvchid = belvchid
    ssettings.banmsgchid = banmsgchid
    ssettings.leavemsgchid = leavemsgchid
    ssettings.kickmsgchid = kickmsgchid
    ssettings.rcmsgchid = rcmsgchid
    ssettings.adminrole = adminrole
    ssettings.roleonjoin = roleonjoin
    ssettings.rssurl = rssurl

    session.add(ssettings)
    session.commit()
    session.close()

def get_servers():
    session = Session()
    query = session.query(Server).all()

    servers = []
    for server in query:
        servers.append({server.dsid : server.sname})

    session.close()

    return servers

def get_settings(sid):
    session = Session()
    query = session.query(ServerSettings).filter_by(sid=sid).all()

    settings = []
    for setting in query:
        settings.append([setting.setid, {setting.sid : [setting.logchid, setting.botcchid, setting.remoj,
                                                        setting.rcount, setting.belvchid, setting.banmsgchid,
                                                        setting.leavemsgchid, setting.kickmsgchid, setting.rcmsgchid,
                                                        setting.adminrole, setting.roleonjoin, setting.rssurl]}])

    session.close()

    return settings