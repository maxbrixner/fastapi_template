# ---------------------------------------------------------------------------- #

import sqlmodel

# ---------------------------------------------------------------------------- #

from test._testcase import TestCase
from app.crud.user import *

# ---------------------------------------------------------------------------- #


class UserCrudTest(TestCase):
    """
    Test cases for CRUD operations in the API.
    """

    def test_create_user(self) -> None:
        """
        Test case for creating a new user.
        """
        result = create_user(
            session=self.session,
            user=UserCreateSchema(
                username="testuser",
                email="test@example.com",
                password="testpassword"
            )
        )
        assert isinstance(result, User)

        user = self.session.exec(sqlmodel.select(User)).first()

        assert user is not None
        assert isinstance(user, User)
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "testpassword"
        assert user.disabled == False


# ---------------------------------------------------------------------------- #
