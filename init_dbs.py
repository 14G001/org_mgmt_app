import subprocess

def get_user_apps(*args):
    apps = []
    for app in args:
        apps.append(app)
        apps.append(f"{app}_example")
    return apps

USER_APPS = get_user_apps("org_mgmt_app", "ensenaxargentina", "exa_teachers")
LOGICAL_APPS = ["user", "organization"]

def runcommand(command):
    print(f"Run: {command}")
    subprocess.run(command, shell=True)

runcommand("rd /s /q .\\user\\migrations .\\organization\\migrations")
DB_FILENAMES = ["db.sqlite3"] + [f"{db}_db.sqlite3" for db in USER_APPS]
for db_filename in DB_FILENAMES:
    runcommand(f"del {db_filename}")
runcommand(
    f"python manage.py makemigrations user"
    f" && python manage.py migrate --database=default")
for db in USER_APPS:
    runcommand(
        f"call env/Scripts/activate"
        f" && python manage.py makemigrations {" ".join(LOGICAL_APPS)}"
        f" && python manage.py migrate --database={db}")