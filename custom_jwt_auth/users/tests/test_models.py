from custom_jwt_auth.users.models import User


class TestUserManger:

    def test_craete_user(self,user: User):
        assert user.is_active == True
        assert user.is_staff == False
        assert user.is_superuser == False

    def test_craete_user2(self, user: User):
        user = user(phone_number="9183404979")
        assert user.phone_number == "9183404979"


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"
