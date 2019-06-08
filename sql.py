from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from helper import isInt

SQL_Base = declarative_base()

class Server(SQL_Base):
    __tablename__ = "Server"

    sid = Column('sid', Integer, primary_key=True)
    dsid = Column('dsid', Integer, nullable=False, unique=True)
    sname = Column('sname', String, nullable=False)
    prefix = Column('prefix', String, nullable=False)

class ServerChannels(SQL_Base):
    __tablename__ = "ServerChannels"

    setid = Column('setid', Integer, primary_key=True)
    sid = Column('sid', Integer, nullable=False, unique=True)

    logchid = Column('logchid', Integer, nullable=False)
    botcchid = Column('botcchid', Integer, nullable=False)
    belvchid = Column('belvchid', Integer, nullable=False)
    banmsgchid = Column('banmsgchid', Integer, nullable=False)
    leavemsgchid = Column('leavemsgchid', Integer, nullable=False)
    kickmsgchid = Column('kickmsgchid', Integer, nullable=False)
    rcmsgchid = Column('rcmsgchid', Integer, nullable=False)
    rsschid = Column('rsschid', Integer, nullable=False)

class ServerSettings(SQL_Base):
    __tablename__ = "ServerSetting"

    setid = Column('setid', Integer, primary_key=True)
    sid = Column('sid', Integer, nullable=False, unique=True)

    remoj = Column('remoj', String, nullable=False)
    rcount = Column('rcount', Integer, nullable=False)
    adminrole = Column('adminrole', String, nullable=False)
    roleonjoin = Column('roleonjoin', String, nullable=False)
    rssurl = Column('rssurl', String, nullable=False)

class Messages(SQL_Base):
    __tablename__ = "Messages"

    msgid = Column('msgid', Integer, primary_key=True)
    dmsgid = Column('dmsgid', Integer, nullable=False, unique=True)
    sid = Column('sid', Integer, nullable=False)
    chid = Column('chid', Integer, nullable=False)
    time = Column('time', Integer, nullable=False)
    content = Column('content', String, nullable=False)
    author = Column('author', String, nullable=False)

class Users(SQL_Base):
    __tablename__ = "Users"

    userid = Column('userid', Integer, primary_key=True)
    duserid = Column('duserid', Integer, nullable=False)
    sid = Column('sid', Integer, nullable=False)


engine = create_engine('sqlite:///servers.db', echo=True)
SQL_Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def create_server(sname, dsid, prefix):
    session = Session()
    server = Server()

    server.sname = sname
    server.dsid = dsid
    server.prefix = prefix

    session.add(server)
    session.commit()
    session.close()

def create_ssettings(sid ,logchid ,botcchid , remoj , rcount , belvchid ,banmsgchid ,leavemsgchid ,kickmsgchid
                     ,rcmsgchid ,adminrole ,roleonjoin ,rssurl, rsschid):
    session = Session()
    ssettings = ServerSettings()
    schannels = ServerChannels()

    intvars = [sid, logchid, botcchid, rcount, belvchid, banmsgchid, leavemsgchid, kickmsgchid, rcmsgchid, rsschid]


    for var in intvars:
        isInt(var, erroring=True)

    ssettings.sid = sid
    schannels.logchid = logchid
    schannels.botcchid = botcchid
    ssettings.remoj = remoj
    ssettings.rcount = rcount
    schannels.belvchid = belvchid
    schannels.banmsgchid = banmsgchid
    schannels.leavemsgchid = leavemsgchid
    schannels.kickmsgchid = kickmsgchid
    schannels.rcmsgchid = rcmsgchid
    ssettings.adminrole = adminrole
    ssettings.roleonjoin = roleonjoin
    ssettings.rssurl = rssurl
    schannels.rsschid = rsschid

    session.add(ssettings)
    session.commit()
    session.close()

def get_servers():
    session = Session()
    query = session.query(Server).all()

    servers = {}
    for server in query:
        servers.update({server.dsid : [server.sname, server.prefix]})

    session.close()

    return servers

def get_settings(sid):
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    settings = []
    settings.append([server.setid, {server.sid : [server.logchid, server.botcchid, server.remoj, server.rcount,
                                                server.belvchid, server.banmsgchid, server.leavemsgchid, server.kickmsgchid,
                                                server.rcmsgchid, server.adminrole, server.roleonjoin, server.rssurl, server.rsschid]}])

    session.close()
    return settings


def edit_prefix(dsid, prefix):
    session = Session()
    server = session.query(Server).filter_by(dsid=dsid).first()

    print(server)

    server.prefix = prefix

    session.commit()
    session.close()

def edit_logchid(sid, logchid):
    isInt(logchid, erroring=True)
    session = Session()
    server = session.query(ServerChannels).filter_by(sid=sid).first()

    server.logchid = logchid

    session.commit()
    session.close()

def edit_botcchid(sid, botcchid):
    isInt(botcchid, erroring=True)
    session = Session()
    server = session.query(ServerChannels).filter_by(sid=sid).first()

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
    isInt(rcount, erroring=True)
    session = Session()
    server = session.query(ServerSettings).filter_by(sid=sid).first()

    server.rcount = rcount

    session.commit()
    session.close()

def edit_belvchid(sid, belvchid):
    isInt(belvchid, erroring=True)
    session = Session()
    server = session.query(ServerChannels).filter_by(sid=sid).first()

    server.belvchid = belvchid

    session.commit()
    session.close()

def edit_banmsgchid(sid, banmsgchid):
    isInt(banmsgchid, erroring=True)
    session = Session()
    server = session.query(ServerChannels).filter_by(sid=sid).first()

    server.banmsgchid = banmsgchid

    session.commit()
    session.close()

def edit_leavemsgchid(sid, leavemsgchid):
    isInt(leavemsgchid, erroring=True)
    session = Session()
    server = session.query(ServerChannels).filter_by(sid=sid).first()

    server.leavemsgchid = leavemsgchid

    session.commit()
    session.close()

def edit_kickmsgchid(sid, kickmsgchid):
    isInt(kickmsgchid, erroring=True)
    session = Session()
    server = session.query(ServerChannels).filter_by(sid=sid).first()

    server.kickmsgchid = kickmsgchid

    session.commit()
    session.close()

def edit_rcmsgchid(sid, rcmsgchid):
    isInt(rcmsgchid, erroring=True)
    session = Session()
    server = session.query(ServerChannels).filter_by(sid=sid).first()

    server.rcmsgchid = rcmsgchid

    session.commit()
    session.close()

def edit_adminrole(sid, adminrole):
    isInt(adminrole, erroring=True)
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

def edit_rsschid(sid, rsschid):
    isInt(rsschid, erroring=True)
    session = Session()
    server = session.query(ServerChannels).filter_by(sid=sid).first()

    server.rsschid = rsschid


def log_msg(dmsgid, sid, chid, time, content, author):
    session = Session()
    message = Messages()

    message.dmsgid = dmsgid
    message.sid = sid
    message.chid = chid
    message.time = time
    message.content = content
    message.author = author

    session.add(message)
    session.commit()
    session.close()

def register_user(duserid, sid):
    session = Session()
    user = Users()

    user.duserid = duserid
    user.sid = sid

    session.add(user)
    session.commit()
    session.close()