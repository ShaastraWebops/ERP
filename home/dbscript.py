import csv
from users.models import *
from django.contrib.auth.models import User
from department.models import *
from django.shortcuts import HttpResponseRedirect

def parse_csv(details):
    line=details.next()
    def parse_line(line):
        print line
        if len(line)==2:
            department=line[0]
            dept=Department(Dept_Name=department)
            dept.save()
            print "saved dept", 
        else:
            try:  
                print line[0], "HERE"
                firstname=line[0].rsplit(' ',1)[0]
                print firstname, "firstname"
                lastname=line[0].rsplit(' ',1)[1]
                print lastname, "lastname"
            except:
                firstname=line[0]
                lastname=''
            print 'firstname', firstname, 'lastname', lastname, 'username', line[1], 'password', line[1]
            user=User(first_name=firstname,last_name=lastname,username=line[1],password=line[1],email=line[2])
            user.save()
            print "saved user", user.first_name
            moreinfo = userprofile(user=user,department=dept,hostel=line[3],name=line[0],chennai_number=line[4])
            moreinfo.save()
            print "saved userprofile", moreinfo.name
        try:
            line=details.next()
            print "Calls again with ", line
            parse_line(line)
        except:
            pass 
    return parse_line(line)
    
def write_into_db(request):
    details=csv.reader(open('home/details.csv', 'rb'))
    print "HERE", details
    parse_csv(details)  
    return HttpResponseRedirect('/')
