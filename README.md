EMIS-project
============

This is a starter project the incorporates basic features of SED-EMIS Project

Getting Started:

    pip install virtualenv
    virtualenv mysiteenv
    source mysiteenv/bin/activate
    pip install Django==1.6.2
    git clone https://prabampm@bitbucket.org/prabampm/emis_dummy.git  emis
    cd emis
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py runserver


Note: Django-mailer has to be installed from source and then run syncdb.. PIP install is broken and gives backend error

Mail Function will not work till you setup cron
#CRON 
#* * * * * (cd /home/praba/web/app/emis/;/home/praba/.virtualenv/emis/bin/python manage.py send_mail >> ~/cron_mail.log 2>&1)
#0,20,40 * * * * (cd /home/praba/web/app/emis/;/home/praba/.virtualenv/emis/bin/python manage.py retry_deferred >> ~/cron_mail_deferred.log 2>&1)
# Edit this file to introduce tasks to be run by cron.
