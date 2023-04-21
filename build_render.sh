#!/bin/bash
pip install Django
pip install django-jsoneditor
pip install numpy
pip install gunicorn
pip install pybedrock==0.0.7
python manage.py collectstatic
