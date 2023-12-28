from sqlalchemy import  Column,PrimaryKeyConstraint, DECIMAL, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class HL7Messages(Base):
    __tablename__ = 'HL7Messages'
    msgid = Column(Integer,primary_key=True)
    importid = Column(Integer)
    message = Column(String)
    rffreport = Column(String)
    status = Column(String)
    exported = Column(Integer)
    notes = Column(String)
    type = Column(Integer)
    userid = Column(String)
    totalcancerterms = Column(Integer)
    totalnegatedcancerterms = Column(Integer)
    processingstatus = Column(Integer)
    reportabilitystatus = Column(Integer)
    autocodingstatus = Column(Integer)
    siteautocoded = Column(Integer)
    behaviourautocoded = Column(Integer)
    histologyautocoded = Column(Integer)
    gradeautocoded = Column(Integer)
    base_msgid = Column(Integer)
    dupflag_import = Column(Integer)
    dupflag_user = Column(Integer)
    lateralityautocoded = Column(Integer)
    reporttype = Column(Integer)
    messagecontrolid = Column(String)
    tempstatus = Column(Integer)



class MSH(Base):
    __tablename__ = 'MSH'
    msgid = Column(Integer, primary_key=True)
    encodingcharacters = Column(String)
    epathdatetimestamp = Column(String)
    fieldseparator = Column(String)
    messagecontrolid = Column(String)
    messagetype = Column(String)
    pathlabid = Column(String)
    pathlabname = Column(String)
    pathlabidcodsystem = Column(String)
    processingid = Column(String)
    versionid = Column(String)
    pathstreet = Column(String)
    pathcity = Column(String)
    pathstate = Column(String)
    pathpostalcode = Column(String)
    transmasterno = Column(String)

class OutputTable(Base):
    __tablename__ = "bccr_outputtable"
    batchid = Column(Integer)
    msgid = Column(Integer)
    predicted_label_id = Column(Integer)
    predicted_label = Column(String)
    model_score = Column(DECIMAL(10,4))
    model_id = Column(String)
    __table_args__ = (
        PrimaryKeyConstraint('batchid', 'msgid'),
    )


class User(Base):
    __tablename__ = "bccr_apiusers"
    useremail = Column(String,primary_key=True)
    password = Column(String)
    profile = Column(String)
    token_exp = Column(Integer)
