from django.contrib.auth.models import User

# TODO: Unhardcode the following main user data:
MAIN_USER_USERNAME = 'bwrXt1N481'
MAIN_USER = {
    'username':MAIN_USER_USERNAME,
    'email':'bwrXt1N481@gmail.com',
    'password':'abc123',
}

main_user_created = False

def create_main_user_if_not_exists():
    global main_user_created
    if main_user_created:
        return
    main_user_created = True
    if User.objects.filter(username=MAIN_USER['username']).exists():
        return
    print('CREATING USER')
    User.objects.create_user(**MAIN_USER)
    