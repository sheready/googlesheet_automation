#configuring the admin console in django to insert records manually
#registering created model class to admin console
script = """ from django.contrib import admin
from .models import * 
"""
#Register your models here.

tables = {}
for model in tables.keys():
    script = script + "admin.site.register(" + model + ")\n"
script

#saving the file
root = 'load_googlesheet/'
file_name = root + 'admin.py'

with open(file_name, "w", encoding='utf-8') as py_file:
    py_file.write(script)