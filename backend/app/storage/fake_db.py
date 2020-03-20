from app.types import UserType

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        # password is 123
        "hashed_password": "$2b$12$kX4B1nJLGX0J6llcYA9LAeLwp6A/k1dBYbLP.7hnoAKmoBpDJSZBK"
    }
}


def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserType(**user_dict)
