def create_models(app, model, records):
    objects = [model(**record) for record in records]
    return model.objects.using(app).bulk_create(objects)

def get_person_id(person):
    return int(person.id%100)+1