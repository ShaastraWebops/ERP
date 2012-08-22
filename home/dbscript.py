import csv
from users.models import *
from django.contrib.auth.models import User
from department.models import *
from django.shortcuts import HttpResponseRedirect

def parse_csv(details):
    line=details.next()
    def parse_line(line,dept=None):
        if len(line)==2:
            department=line[0]
            dept=Department(Dept_Name=department)
            dept.save()
            try:
                line=details.next()
                save_user(line,dept)
            except:
                pass
        else:
            save_user(line,dept)
            
    def save_user(line,dept):
        try:  
            firstname=line[0].rsplit(' ',1)[0]
            lastname=line[0].rsplit(' ',1)[1]
        except:
            firstname=line[0]
            lastname=''
        print 'firstname', firstname, 'lastname', lastname, 'username', line[1], 'password', line[1], 'email', line[2], 'dept', dept
        user=User()
        user.first_name=firstname
        user.last_name=lastname
        user.username=line[1].lower()
        user.password=line[1].lower()
        user.email=line[2]
        user.save()
        moreinfo = userprofile(user=user,department=dept,hostel=line[3],name=line[0],chennai_number=line[4])
        moreinfo.save()
        try:
            line=details.next()
            print "Call with", line
            parse_line(line,dept)
        except:
            pass 
    return parse_line(line)
    
def write_into_db(request):
    details=csv.reader(open('home/details.csv', 'rb'))
    print details
    parse_csv(details)  
    return HttpResponseRedirect('/')
