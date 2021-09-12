"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from config import get_config_ipdb_break
import ipdb
# if get_config_ipdb_break(): ipdb.set_trace()

from models import db, Message, User, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

# os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        # if get_config_ipdb_break(): ipdb.set_trace()

        Likes.query.delete()
        Message.query.delete()
        User.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        db.session.commit()


    def test_unauthorized(self):
        """Can access message page?"""
        # if get_config_ipdb_break(): ipdb.set_trace()

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:

            resp = c.get("/messages/new")

            # can the page be found?
            self.assertEqual(resp.status_code, 302)

            html = resp.get_data(as_text=True)

            # is there authorization?
            self.assertIn('You should be redirected automatically to target URL:', html)


    def test_unauthorized_post(self):
        """Can't post to message page?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:

            # if get_config_ipdb_break(): ipdb.set_trace()
            resp = c.post("/messages/new", data={"text": "Hello"})

            self.assertEqual(resp.status_code, 302)

            html = resp.get_data(as_text=True)

            # is there authorization?
            self.assertIn('You should be redirected automatically to target URL:', html)


    def test_add_message(self):
        """Can user post a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")


    def test_list_message(self):
        """Can view user's posted message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            if get_config_ipdb_break(): ipdb.set_trace()

            resp = c.get(f"/users/{self.testuser.id}")
            html = resp.get_data(as_text=True)
            self.assertNotIn('Hello', html)

            resp = c.post("/messages/new", data={"text": "Hello"})

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

            resp = c.get(f"/users/{self.testuser.id}")
            html = resp.get_data(as_text=True)
            self.assertIn('Hello', html)
