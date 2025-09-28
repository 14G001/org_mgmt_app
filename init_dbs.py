import subprocess

def get_app_versions(*args):
    apps = []
    for app in args:
        apps.append(app)
        apps.append(f"{app}_example")
    return apps

ORG_MGMT_USER_APPS = get_app_versions("org_mgmt_app", "exa_org_mgmt_app")
EXA_APPS           = get_app_versions("ensenaxargentina")
USER_APPS = ORG_MGMT_USER_APPS + EXA_APPS

def runcommand(command):
    print(f"Run: {command}")
    subprocess.run(command, shell=True)
def del_migrations(*args):
    runcommand(f"rd /s /q {" ".join([f".\\{app}\\migrations" for app in args])}")
def migrate(logical_app, app):
    runcommand(
        f"call env/Scripts/activate"
        f" && python manage.py makemigrations {logical_app}"
        f" && python manage.py migrate --database={app}")

del_migrations("user", "org_mgmt_app", "ensenaxargentina")
DB_FILENAMES = ["db.sqlite3"] + [f"{db}_db.sqlite3" for db in USER_APPS]
for db_filename in DB_FILENAMES:
    runcommand(f"del {db_filename}")
migrate("user", "default")
for app in ORG_MGMT_USER_APPS:
    migrate("org_mgmt_app", app)
migrate("ensenaxargentina", "default")