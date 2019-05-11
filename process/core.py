from model import Email, engine
from sqlalchemy.orm import sessionmaker


DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_all_emails():
    all_email_objects = session.query(Email).all()
    return all_email_objects


def update_email_label(message_id: str, label: str) -> None:
    message = session.query(Email).filter(Email.message_id == message_id).first()
    message.label = label
    session.commit()

