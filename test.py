import unittest
from model import Email, create_engine, ROOT_DIR, Base
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from process import composed, core

test_engine = create_engine(f'sqlite:///{ROOT_DIR}/sqlite_test.db')


class TestEmail(unittest.TestCase):

    def setUp(self):
        DBSession = sessionmaker(bind=test_engine)
        Base.metadata.create_all(test_engine)
        session = DBSession()
        email_obj = Email(
            from_address="drb@gmail.com",
            to_address="foo@gmail.com",
            is_read=True,
            is_archived=True,
            subject="test",
            message_body="test",
            message_id="test",
            label="INBOX",
            has_attachment=False,
            received_on=datetime.now()
        )
        session.add(email_obj)
        session.commit()

    def test_extract_single_email(self):

        single_email = composed.extract_single_message(mail_id=1)

        self.assertEqual(single_email["id"], 1)
        self.assertEqual(single_email["message_id"], "test")
        self.assertEqual(single_email["has_attachment"], False)
        self.assertEqual(single_email["message_body"], "test")
        self.assertEqual(single_email["label"], "INBOX")
        self.assertEqual(single_email["from_address"], "drb@gmail.com")
        self.assertEqual(single_email["to_address"], "foo@gmail.com")
        self.assertEqual(single_email["is_read"], True)
        self.assertEqual(single_email["is_archived"], True)
        self.assertIsNotNone(single_email["received_on"])

    def test_get_all_emails(self):
        all_emails = core.get_all_emails()

        self.assertGreater(len(all_emails), 0)

    def test_extract_query_set(self):

        email_list = composed.extract_email_queryset()

        self.assertGreater(len(email_list), 0)

    def test_update_email_label(self):
        core.update_email_label(message_id="test", label="INBOX")
        single_email = composed.extract_single_message(mail_id=1)

        self.assertEqual(single_email["label"], "INBOX")

    def test_update_archive_status(self):
        core.change_archive_status(message_id="test", status=True)
        single_email = composed.extract_single_message(mail_id=1)

        self.assertNotEqual(single_email["is_archived"], False)


if __name__ == '__main__':
    unittest.main()
