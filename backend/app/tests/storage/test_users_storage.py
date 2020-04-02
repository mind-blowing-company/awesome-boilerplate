from unittest import TestCase

from app.storage.db.database_storage import DatabaseStorage
from app.storage.models import User


class UsersStorageTestCase(TestCase):
    def setUp(self):
        self.storage = DatabaseStorage(User, "sqlite://")

    def test_creates_user(self):
        user_to_create = User(
            username="JohnDoe",
            password="password",
            email="johndoe@gmail.com"
        )
        db_user = self.storage.create(user_to_create)

        self.assertEqual(db_user.id, 1)
        self.assertEqual(db_user.email, user_to_create.email)
        self.assertEqual(db_user.username, user_to_create.username)
        self.assertEqual(db_user.password, user_to_create.password)

    def test_gets_user(self):
        user_to_create = User(
            username="JohnDoe",
            password="password",
            email="johndoe@gmail.com"
        )
        self.storage.create(user_to_create)

        user_from_db = self.storage.get(id=1)

        self.assertEqual(user_from_db.username, user_to_create.username)
        self.assertEqual(user_from_db.password, user_to_create.password)
        self.assertEqual(user_from_db.email, user_to_create.email)

    def test_updates_user(self):
        db_user = self.storage.create(User(
            username="JohnDoe",
            password="password",
            email="johndoe@gmail.com"
        ))

        db_user.email = "random@gmail.com"
        db_user.password = "new-password"
        db_user.username = "Jane"

        updated_user = self.storage.update(db_user)

        self.assertEqual(updated_user.id, db_user.id)
        self.assertEqual(updated_user.username, "Jane")
        self.assertEqual(updated_user.password, "new-password")
        self.assertEqual(updated_user.email, "random@gmail.com")
