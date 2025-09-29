from user.models import User

TEST_USERS_PASSWORD = "abc123"

def create_test_user(app, user_type, username, name):
    return User.objects.create_user(
        app, f"{username}@test.com", username, TEST_USERS_PASSWORD,
        user_type, name, "TstSnm")