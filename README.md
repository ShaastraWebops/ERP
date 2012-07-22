Shaastra ERP
============

The Shaastra ERP is an Enterprise Resource Planner for IIT Madras' techfest, Shaastra.

Install Haystack 1.2.6. If you decide to go with Haystack 2.0 remove the HAYSTACK_CONF and the other haystack settings and replace with <a href"http://dpaste.com/759934/"> this</a>.
There are some other instructions on the doc <a href="http://django-haystack.readthedocs.org/en/latest/tutorial.html#configuration"> here</a>.<br><br>
Install Whoosh. <br><br>
Follow the following steps if you've just created/recreated your database for the ERP:
*Run python manage.py syncdb. Create a superuser if you wish.<br>
*Go to to media/upload_files in the erp folder and delete all folders and files there. You need to do this to ensure that the right entries are created in the next few steps.<br>
*Run python manage.py runserver<br>
*Go to localhost:8000/loaddata and wait for the "Done" message. This loads the database with the test data.<br>
*Run python manage.py rebuild_index. This indexes the tasks, so that search works.<br><br>
The landing page is at localhost:8000/.<br><br>
The test data creates test users from 'ee09b001' to 'ee09b030'. The passwords for all these users is 'default'.
