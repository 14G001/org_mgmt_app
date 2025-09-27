import subprocess

DBS          = [              "org_mgmt_app"           , "org_mgmt_app_example"           , "ensenaxargentina"           , "ensenaxargentina_example"           ]
DB_FILENAMES = ["db.sqlite3", "org_mgmt_app_db.sqlite3", "org_mgmt_app_example_db.sqlite3", "ensenaxargentina_db.sqlite3", "ensenaxargentina_example_db.sqlite3"]
APPS = ["user", "organization"]

def runcommand(command):
    print(f"Run: {command}")
    subprocess.run(command, shell=True)

runcommand("rd /s /q .\\user\\migrations .\\organization\\migrations")
for db_filename in DB_FILENAMES:
    runcommand(f"del {db_filename}")
runcommand(
    f"python manage.py makemigrations user"
    f" && python manage.py migrate --database=default")
for db in DBS:
    runcommand(
        f"call env/Scripts/activate"
        f" && python manage.py makemigrations {" ".join(APPS)}"
        f" && python manage.py migrate --database={db}")