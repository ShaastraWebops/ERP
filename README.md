ERP
===

This contains the source code of ERP 

Install Haystack 1.2.6. If you decide to go with Haystack 2.0 remove the HAYSTACK_CONF and the other haystack settings and replace with
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
} <br>
There are some other instructions on the doc <a href="http://django-haystack.readthedocs.org/en/latest/tutorial.html#configuration"> here </a><br>
Install Whoosh. <br>
Once the dev server is running, you'll see that the UserProfile is not being written. Write in some entries to UserProfile and Tasks.<br>
Now run manage.py rebuild_index. This will index the new entries that you wrote to Tasks.<br>
Go to localhost:8000/erp. Once you login, you'll be prompted for the shaastra.org login details because of frontend material. Provide the CP login or avoid this altogether by changing the URLs in settings to your local comp<br>
Login using admin.(The register/create a new account wasn't working for me)<br>
Go to localhost:8000/search. Search for the task that you set before. It'll give you weird results.<br>
Play around with the dashboard :)