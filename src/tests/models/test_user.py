import pytest
from data.models import User

@pytest.mark.usefixtures('db')
class TestUser:

    def test_password_setter(self):
        u = User(password='cat')
        assert u.password_hash is not None

    def test_no_password_getter(self):
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
