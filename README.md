Shaastra ERP
============

The Shaastra ERP is an Enterprise Resource Planner for IIT Madras' techfest, Shaastra.

Install Haystack 1.2.6. If you decide to go with Haystack 2.0 remove the HAYSTACK_CONF and the other haystack settings and replace with <a href"http://dpaste.com/759934/"> this</a>.
There are some other instructions on the doc <a href="http://django-haystack.readthedocs.org/en/latest/tutorial.html#configuration"> here</a>.<br><br>
Install Whoosh. <br><br>
Once the dev server is running, got to localhost:8000/loaddata and wait for the "Done" message. This loads the database with the test data.<br><br>
Now run manage.py rebuild_index. This will index the new Tasks.<br><br>
The landing page is at localhost:8000/.<br><br>
If you'd like to login as a specific user, use the Django admin to set the password for the desired user, and then login.<br><br>
Search functionality is currently enabled at localhost:8000/search, due to default templates and views being used.
