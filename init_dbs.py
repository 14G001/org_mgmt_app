import subprocess

def get_user_apps(*args):
    apps = []
    for app in args:
        apps.append(app)
        apps.append(f"{app}_example")
    return apps

ORG_MGMT_USER_APPS = get_user_apps("org_mgmt_app", "ensenaxargentina")
USER_APPS = ORG_MGMT_USER_APPS + get_user_apps("exa_teachers")

def runcommand(command):
    print(f"Run: {command}")
    subprocess.run(command, shell=True)
def migrate(logical_app, app):
    runcommand(
        f"call env/Scripts/activate"
        f" && python manage.py makemigrations {logical_app}"
        f" && python manage.py migrate --database={app}")

runcommand("rd /s /q .\\user\\migrations .\\org_mgmt_app\\migrations .\\exa_teachers\\migrations")
DB_FILENAMES = ["db.sqlite3"] + [f"{db}_db.sqlite3" for db in USER_APPS]
for db_filename in DB_FILENAMES:
    runcommand(f"del {db_filename}")
migrate("user", "default")
for app in ORG_MGMT_USER_APPS:
    migrate("org_mgmt_app", app)
migrate("exa_teachers", "exa_teachers")