from model import Email, engine
from sqlalchemy.orm import sessionmaker


DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_all_emails():
    all_email_objects = session.query(Email).all()
    return all_email_objects

