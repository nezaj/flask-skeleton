import pytest

from datetime import datetime, timedelta
from src.data.models import User, UserPasswordToken
from .generate import generate_user

@pytest.fixture
def user(db):
    return generate_user().save(db.session)

def expired_date():
    return datetime.utcnow() + timedelta(seconds=-1)

class TestUserPasswordToken:

    def test_used_token_is_not_valid(self, user, db):
        # Newly generated token is valid
        token = UserPasswordToken(user=user).save(db.session)
        assert token.invalid is False

        # Used token is not valid
        token.update(used=True)
        assert token.invalid is True

    def test_expired_token_is_not_valid(self, user, db):
        # Newly generated token is valid
        token = UserPasswordToken(user=user).save(db.session)
        assert token.invalid is False

        # Expired token is not valid
        token.update(expiration_dt=expired_date())
        token.save(db.session)
        assert token.invalid is True

    def test_valid_token(self, user, db):
        # Valid token is found
        invalid_token = UserPasswordToken(user=user, used=True).save()
        valid_token = UserPasswordToken(user=user).save()
        assert UserPasswordToken.valid_token(user.id) == valid_token

    def test_invalid_tokens(self, user, db):
        # Invalid tokens
        used_token = UserPasswordToken(user=user, used=True).save()
        expired_token = UserPasswordToken(user=user, expiration_dt=expired_date()).save()

        # Valid token
        valid_token = UserPasswordToken(user=user, used=False).save()

        # All invalid tokens for a user are captured
        invalid_tokens = set(UserPasswordToken.invalid_tokens(user_id=user.id).all())
        assert invalid_tokens == set([used_token, expired_token])

    def test_get_or_create_token(self, user, db):
        user_tokens_query = db.session.query(UserPasswordToken).filter_by(user_id=user.id)

        # No tokens are present for a newly created user
        user_tokens_query.all() == []

        # A new token is created when none are present
        token = UserPasswordToken.get_or_create_token(user.id)
        assert user_tokens_query.all() == [token]

        # The same token is returned while it is still valid.
        assert UserPasswordToken.get_or_create_token(user.id) == token
        assert user_tokens_query.count() == 1

        # A new token is created once the old one is used. This new token is the only token for that user.
        token.update(used=True)
        unused_token = UserPasswordToken.get_or_create_token(user.id)
        assert unused_token != token
        assert user_tokens_query.count() == 1

        # A new token is created once the old one is expired. This new token is the only token for that user.
        unused_token.update(expiration_dt=expired_date())
        unexpired_token = UserPasswordToken.get_or_create_token(user.id)
        assert unexpired_token != token
        assert unexpired_token != unused_token
        assert user_tokens_query.count() == 1

    def test_token_values_unique(self, user, db):
        # Tokens have different values
        t1 = UserPasswordToken(user=user).save()
        t2 = UserPasswordToken(user=user).save()
        assert t1.value != t2.value

    def test_unique_expiration_dt(self, user, db):
        # Tokens created at different times have different expiration dates
        t1 = UserPasswordToken(user=user).save()
        t2 = UserPasswordToken(user=user).save()
        assert t1.expiration_dt != t2.expiration_dt
