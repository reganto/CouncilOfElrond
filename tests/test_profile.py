from app import Application
from tests.base import BaseTest
from database.models import User, Thread,  migrator
from database.model_factory import Factory


class ProfilesTest(BaseTest):
    def get_app(self):
        return Application()

    def setUp(self):
        super().setUp()
        migrator.upgrade()

    def tearDown(self):
        super().tearDown()
        migrator.downgrade()

    def field(self, f: str) -> bytes:
        return bytes(f.encode())

    def test_a_user_has_a_profile(self):
        user = Factory(User).create()
        response = self.fetch(f'/profiles/{user.username}/')
        self.assertIn(self.field(user.username), response.body)

    def test_profiles_display_all_threads_by_associated_user(self):
        user = Factory(User).create()
        thread = Factory(Thread).create()
        thread.user_id = user
        thread.save()

        response = self.fetch(f'/profiles/{user.username}')
        self.assertIn(self.field(thread.title), response.body)
        self.assertIn(self.field(thread.body), response.body)

