from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pytz import timezone
import os
from sqlalchemy import create_engine
tz = timezone('Asia/Calcutta')
Base = declarative_base()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_datetime():
    return datetime.now(tz=tz)


class Email(Base):
    __tablename__ = 'email'
    # Here we define columns for the table email
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String(250), nullable=False)
    from_address = Column(String(250), nullable=False)
    to_address = Column(String(250), nullable=False)
    subject = Column(String(250), nullable=True)
    message_body = Column(Text(), nullable=True)
    is_read = Column(Boolean(), nullable=False)
    label = Column(Text(), nullable=True)
    is_archived = Column(Boolean(), nullable=False)
    has_attachment = Column(Boolean(), default=False)
    received_on = Column(DateTime(), nullable=False)
    created_on = Column(DateTime(), nullable=False, default=get_datetime)
    updated_on = Column(DateTime(), nullable=False, default=get_datetime, onupdate=get_datetime)

    def __init__(self, message_id, from_address, to_address, subject,
                 message_body, is_read, label, is_archived, received_on, has_attachment):
        self.message_id = message_id
        self.from_address = from_address
        self.to_address = to_address
        self.subject = subject
        self.message_body = message_body
        self.is_read = is_read
        self.label = label
        self.is_archived = is_archived
        self.received_on = received_on
        self.has_attachment = has_attachment


engine = create_engine(f'sqlite:///{ROOT_DIR}/sqlite.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
