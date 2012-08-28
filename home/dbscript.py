import csv
from users.models import *
from django.contrib.auth.models import User, Group
from department.models import *
from django.shortcuts import HttpResponseRedirect
import string
import random

# Write each entry to the CSV
def writeout(writer,username, password, email):
    writer.writerow([username, password, email])

# Generate a lowercase+digit sequence of SIZE 
def pass_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def parse_csv(details,writer):
    ''' 
    Reads the CSV line by line and parses it based on length.
    This is not very elegant and changing the format of the CSV
    will force changes in code. Please look at home/details.csv
    for format.
    '''
    line=details.next()
    def parse_line(line,dept=None):
        # This row will then mean a new department.
        if len(line)==2:
            dept=Department(Dept_Name=line[0])
            dept.save()
            try:
                line=details.next()
                save_user(line,dept)
            except:
                pass
        else:
            save_user(line,dept)
    # Save the details of user to DB and call csvwrite        
    def save_user(line,dept):
        # Very rough and ugly name parser.
        try:  
            firstname=line[0].rsplit(' ',1)[0]
            lastname=line[0].rsplit(' ',1)[1]
        except:
            firstname=line[0]
            lastname=''
        print 'Firstname:', firstname, '\nLastname:', lastname, '\nUsername:', line[1], '\nEmail:', line[2], '\nDept:', dept
        user=User()
        user.first_name=firstname
        user.last_name=lastname
        user.username=line[1].lower()
        password = pass_generator(size=8)
        #Hash the password and save
        user.set_password(password)
        user.email=line[2]
        user.save()
        # Currently everyone in the CSV are COORDS. Change if otherwise
        user.groups.add(Group.objects.get(name='Coord'))
        # write to CSV
        writeout(writer,user.username,password,user.email)
        moreinfo = userprofile(user=user,department=dept,hostel=line[3],name=line[0],chennai_number=line[4])
        moreinfo.save()

        try:
            # Incase end of file? Very ugly but I can't find any other way
            line=details.next()
            parse_line(line,dept)
        except:
            pass 
    return parse_line(line)

# Open one to read and one to write    
def write_into_db(request):
    details=csv.reader(open('home/details.csv', 'rb'))
    outfile=open('home/lookup.csv', 'wb')
    writer = csv.writer(outfile)
    # Create group if already not there
    Group.objects.get_or_create(name='Coord')
    parse_csv(details,writer)  
    # only closing saves the csv. NOTE: breaking out of the process midway will not save the passes.
    outfile.close()
    return HttpResponseRedirect('/')
