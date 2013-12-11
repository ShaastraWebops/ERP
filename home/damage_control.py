from django.contrib.auth.models import User
import csv
import string
import random

def do_it():
    users=User.objects.all()
    outfile=open('home/maillist.csv','wb')
    writer=csv.writer(outfile)
    print "doing it"
    for user in users:
        if not user.is_superuser:
            password=pass_generator(8)
            user.set_password(password)
            user.save()
            writer.writerow([user.username, user.email, password])
    outfile.close()

def pass_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
