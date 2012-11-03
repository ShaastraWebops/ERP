from django.core.mail import send_mail, send_mass_mail
from django.shortcuts import HttpResponseRedirect
import csv
from users.models import *
from django.core.mail import EmailMultiAlternatives

def send_mail():   
    subject, from_email= 'Shaastra-ERP login details', 'ShaastraERP'
    #to =['swapnilbasak@yahoo.com']
    details=csv.reader(open('home/maillist-2.csv', 'rb'))
    f=open('home/Erp_writeup.txt')
    #t=open('home/Erp_writeup_text.txt')
    html = f.read()
    #text = t.read()
    message=[]
    line=details.next()
    stream=True
    while(stream):
        to = [line[1]]
        user = line[0]
        password = line[2]
        text_content = 'If you are seeing this, you mail client does not support html and that is,... embarrassing.'
        html_content = html.replace('<<username>>',user).replace('<<password>>',password)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)   
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print "Sent to", user, "at", to
        with open("home/completed.txt", "a") as completed:
            completed.write(to[0]+'')
            completed.close()
        try:
            line=details.next()
        except: 
            stream=False 
    return 1
    
