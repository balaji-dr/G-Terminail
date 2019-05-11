from model import Email, engine
from sqlalchemy.orm import sessionmaker
from typing import List, Dict

DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_all_emails():
    all_email_objects = session.query(Email).all()
    return all_email_objects


def update_email_label(message_id: str, label: str) -> None:
    message = session.query(Email).filter(Email.message_id == message_id).first()
    message.label = label
    session.commit()


def update_email_status(message_id: str, label: str) -> None:
    message = session.query(Email).filter(Email.message_id == message_id).first()
    label_list: List = label.split(',')
    if "UNREAD" not in label_list:
        message.is_read = True
    else:
        message.is_read = False
    session.commit()


def change_archive_status(message_id: str, status: bool) -> None:
    message = session.query(Email).filter(Email.message_id == message_id).first()
    message.is_archived = status
    session.commit()
