from model import Email, engine
from sqlalchemy.orm import sessionmaker
from typing import List

DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_all_emails():
    """
    Gets all the email records from the database.
    :return: QuerySet containing all the records.
    """
    all_email_objects = session.query(Email).all()
    return all_email_objects


def update_email_label(message_id: str, label: str) -> None:
    """
    Updates the email with the given label.
    :param message_id: Id of the message stored in the database.
    :type message_id: str
    :param label: Label to be updated.
    :type label: str
    :return: None
    """
    message = session.query(Email).filter(Email.message_id == message_id).first()
    message.label = label
    session.commit()


def update_email_status(message_id: str, label: str) -> None:
    """
    Updates the email with the given status - Read/Unread.
    :param message_id: Id of the message stored in the database.
    :type message_id: str
    :param label: Label to be updated - Read/UnRead.
    :type label: str
    :return: None
    """
    message = session.query(Email).filter(Email.message_id == message_id).first()
    label_list: List = label.split(',')
    if "UNREAD" not in label_list:
        message.is_read = True
    else:
        message.is_read = False
    session.commit()


def change_archive_status(message_id: str, status: bool) -> None:
    """
    Update the archive status of the stored email.
    :param message_id: Id of the message stored in the database.
    :type message_id: int
    :param status: Archive status.
    :type status: bool
    :return: None
    """
    message = session.query(Email).filter(Email.message_id == message_id).first()
    message.is_archived = status
    session.commit()


def get_single_message_object(mail_id: int) -> Email:
    """
    Get single mail object from the database.
    :param mail_id: Id of the message stored in the database.
    :return: Email object.
    """
    message = session.query(Email).filter(Email.id == mail_id).first()
    return message
