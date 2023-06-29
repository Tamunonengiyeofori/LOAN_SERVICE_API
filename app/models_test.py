from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine 

from sqlalchemy import Column, Integer, String, ForeignKey

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:22of22in22@localhost:5432/loan_service"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id  = Column(Integer, autoincrement=True, primary_key=True)
    jobs = relationship("Job", back_populates="user")
    
class Audio(Base):
    __tablename__ = "audios"
    id = Column(Integer, autoincrement=True, primary_key=True)
    # agent_id = Column(Integer, autoincrement=True, server_default=56, unique=True)
    audio_record = Column(String(80))
    job = relationship("Job", back_populates="audio_record", uselist=False)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, autoincrement=True, primary_key=True)    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="jobs")
    audio_id = Column(Integer, ForeignKey("audios.id", ondelete="CASCADE"), unique=True)
    audio_record= relationship("Audio", back_populates="job")
    # transcript = relationship("Transcript", back_populates="job", uselist=False)

class Transcript(Base):
    __tablename__ = "transcripts"
    id = Column(Integer, autoincrement=True, primary_key=True)
    transcript_id = Column(Integer, ForeignKey("jobs.id" , ondelete="CASCADE"), unique=True) 
    transcript_text = Column(String(255))
    # job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), unique=True)
    # job = relationship("Job", back_populates="transcript")
    
    
class Sentiment(Base):
    __tablename__ = "sentiments"
    id = Column(Integer, autoincrement=True, primary_key=True)
    sentiment_id = Column(Integer, ForeignKey("transcripts.transcript_id"))
    response = relationship("Response", back_populates="sentiment")
    response_id = Column(Integer, ForeignKey("response.id"))
    
class Response(Base):
    __tablename__ = "response"
    id = Column(Integer, autoincrement=True, primary_key=True)
    friendly_score = Column(Integer)
    customer_satisfaction = Column(Integer)
    sentiment = relationship("Sentiment", back_populates="response", uselist=False)
    
