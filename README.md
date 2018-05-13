To install
virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt

To migrate the DB
python manage.py migrate

To collect the statics for production
python manage.py collectstatic

To install the cron jobs
- Make sure to copy the hash that identifies the email job
python manage.py crontab add

To execute the jobs in Python Anywhere:
- Add a task that executes the cron job with the hash reference from the last step. Example:
    /home/Tzesar/.virtualenvs/realEstate-venv/bin/python /home/Tzesar/realEstate/manage.py crontab run 728ab3ac1c9515a312d2d8097e7313f5