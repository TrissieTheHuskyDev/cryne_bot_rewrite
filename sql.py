from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    settings = []
    settings.append([server.setid, {server.sid : [server.logchid, server.botcchid, server.remoj, server.rcount,
                                                server.belvchid, server.banmsgchid, server.leavemsgchid, server.kickmsgchid,
                                                server.rcmsgchid, server.adminrole, server.roleonjoin, server.rssurl]}])

    session.close()
    return settings


def edit_logchid(sid, logchid):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.logchid = logchid

    session.commit()
    session.close()

def edit_botcchid(sid, botcchid):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.botcchid = botcchid

    session.commit()
    session.close()

def edit_remoj(sid, remoj):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.remoj = remoj

    session.commit()
    session.close()

def edit_rcount(sid, rcount):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.rcount = rcount

    session.commit()
    session.close()

def edit_belvchid(sid, belvchid):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.belvchid = belvchid

    session.commit()
    session.close()

def edit_banmsgchid(sid, banmsgchid):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.banmsgchid = banmsgchid

    session.commit()
    session.close()

def edit_leavemsgchid(sid, leavemsgchid):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.leavemsgchid = leavemsgchid

    session.commit()
    session.close()

def edit_kickmsgchid(sid, kickmsgchid):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.kickmsgchid = kickmsgchid

    session.commit()
    session.close()

def edit_rcmsgchid(sid, rcmsgchid):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.rcmsgchid = rcmsgchid

    session.commit()
    session.close()

def edit_adminrole(sid, adminrole):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.adminrole = adminrole

    session.commit()
    session.close()

def edit_roleonjoin(sid, roleonjoin):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.roleonjoin = roleonjoin

    session.commit()
    session.close()

def edit_rssurl(sid, rssurl):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.rssurl = rssurl

    session.commit()
    session.close()