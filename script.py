import os
import time
from pathlib import Path

project_name = input("Enter project name:")
app_name = input("Enter app name:")

# project_name = "new_project"
# app_name= 'core'

cwd = Path.cwd()
project_path = cwd / project_name

if not project_path.is_dir():
    os.system("django-admin startproject "+project_name)


os.chdir(project_path)
app_path= project_path/app_name


if not app_path.is_dir():
    os.system("python manage.py startapp "+ app_name)


app_urls_path = app_path / 'urls.py'
app_urls_path.touch()

settings_path = project_path/project_name/'settings.py'


with open(settings_path ,'r') as f:
    data = f.readlines()
f.close()

app_name_modified = f"'{app_name}'"
with open(settings_path,'w+') as f:
    for i in data:
        if i == "INSTALLED_APPS = [\n":
            i += "    "+app_name_modified+",\n"
        f.write(i)
f.close()
