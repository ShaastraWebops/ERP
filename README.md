ERP
===

This contains the source code of ERP 

Install Haystack 1.2.6. If you decide to go with Haystack 2.0 remove the HAYSTACK
Install Whoosh. 
Once the dev server is running, you'll see that the UserProfile is not being written. Write in some entries to UserProfile and Tasks.
Now run manage.py rebuild_index. This will index the new entries that you wrote to Tasks.
Go to localhost:8000/erp. Once you login, you'll be prompted for the shaastra.org login details because of frontend material. Provide the CP login or avoid this altogether by changing the URLs in settings to your local comp
Login using admin.(The register/create a new account wasn't working for me)
Go to localhost:8000/search. Search for the task that you set before. It'll give you weird results.
Play around with the dashboard :)