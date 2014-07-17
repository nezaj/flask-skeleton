import pytest
from sqlalchemy.exc import IntegrityError
from src.data.models import User

from .generate import generate_user

class TestUser:

    def test_password_setter(self):
        "Setting password generates a password hash"
        u = User(password='cat')
        assert u.password_hash is not None

    def test_no_password_getter(self):
        "Password should not be directly accessible"
        u = User(password='cat')
        with pytest.raises(AttributeError):
            u.password  # pylint: disable=W0104

    def test_password_verification(self):
        u = User(password='cat')
        assert u.verify_password('cat') is True
        assert u.verify_password('dog') is False

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        assert u.password_hash != u2.password_hash

    def test_user_emails_unique(self, db):
        "Two users saved with same email should raise an error"
        email = "bob@example.com"
        u1 = generate_user(email=email, username="bob")
        u2 = generate_user(email=email, username="jane")
        u1.save()
        with pytest.raises(IntegrityError):
            u2.save()

        # This should be fine
        db.session.rollback()
        u2.email = "jane@example.com"
        u2.save()

    def test_usernames_unique(self, db):
        "Two users saved with same username should raise an error"
        username= "bob"
        u1 = generate_user(email="bob@example.com", username=username)
        u2 = generate_user(email="jane@example.com", username=username)
        u1.save()
        with pytest.raises(IntegrityError):
            u2.save()

        db.session.rollback()
        u2.username = "jane"
        u2.save()

    def test_activate_tokens_unique(self, db):
        u1 = generate_user(email="bob@example.com", username='bob').save()
        u2 = generate_user(email="jane@example.com", username='jane').save()
        assert u1.activate_token != u2.activate_token

    def test_find_by_email(self, db):
        email = "bob@example.com"
        u1 = generate_user(email=email)
        u1.save()
        assert User.find_by_email(email) == u1

    def test_find_by_username(self, db):
        username = "bob"
        u1 = generate_user(username=username)
        u1.save()
        assert User.find_by_username(username) == u1
