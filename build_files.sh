#!/bin/bash
pip install scikit-build==0.16.7
pip install -r requirements.txt
python3.9 manage.py collectstatic