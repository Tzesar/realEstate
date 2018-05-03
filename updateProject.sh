#!/bin/bash

git fetch --all
git checkout development
git pull origin development

python manage.py collectstatic
