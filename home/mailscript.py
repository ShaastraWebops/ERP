from django.core.mail import send_mail, send_mass_mail
from django.shortcuts import HttpResponseRedirect
import csv
from users.models import *
from django.core.mail import EmailMultiAlternatives

def send_mail(request):   
    subject, from_email= 'Shaastra-ERP login details', 'ShaastraERP@iitm.ac.in'
    #to =['swapnilbasak@yahoo.com']
    details=csv.reader(open('home/coremaillist.csv', 'rb'))
    f=open('home/Core_writeup.txt')
    #t=open('home/Erp_writeup_text.txt')
    html = f.read()
    print html
    #text = t.read()
    message=[]
    line=details.next()
    stream=True
    while(stream):
        to = [line[1]]
        user = line[0]
        password = line[2]
        print "Sent to", user, "at", to
        text_content = 'If you are seeing this, you mail client does not support html and that is,... embarrassing.'
        html_content = html.replace('<<username>>',user).replace('<<password>>',password)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)   
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        with open("home/completed.txt", "a") as completed:
            completed.write(to[0]+'')
            completed.close()
        try:
            line=details.next()
        except: 
            stream=False 
    return HttpResponseRedirect('/')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#    details=csv.reader(open('home/lookup.csv', 'rb'))
#    message=[]
#    line=[]
#    stream=True
#    while(stream):
#        message.extend(('Shaastra|ERP Login Details', 'Here is the message', 'from@iitm.ac.in', ['swapnilbasak@gmail.com', ##'swapnilbasak@yahoo.com']))
 #       message.extend(('Another Subject', 'Here is another message', 'from@iitm.ac.in', ['swapnilbasak@yahoo.com']))
 #       try:
 #           line=details.next()
  #      except:
  #          stream=False
  #  #send_mass_mail((message1, message2), fail_silently=False)
  #  print line
  #  return HttpResponseRedirect('/')
