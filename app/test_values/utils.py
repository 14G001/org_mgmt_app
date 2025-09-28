from user.models import User

def create_models(app, model, records):
    objects = [model(**record) for record in records]
    return model.objects.using(app).bulk_create(objects)

def create_test_user(app, user_type, username):
    return User.objects.create_user(
        app, f"{username}@test.com", username, "abc123", user_type)

def get_person_id(person):
    return int(person.id%100)+1