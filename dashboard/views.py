# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.utils.translation import ugettext as _
from django.core.mail import send_mail,EmailMessage,SMTPConnection
from django.contrib.sessions.models import Session
from erp.dashboard.models import *
from erp.dashboard.forms import *
from erp.department.models import *
from erp.users.models import *
from erp.users.views import *
from erp.tasks.views import *
from erp.misc.util import *
from erp.settings import *
import sha,random,datetime
from erp.dashboard.forms import *
from erp.users.forms import *
import os # upload files
from django.conf import settings
from django.utils import simplejson
import csv # invite coords
#import stringlib


"""

Common Tab - a tab which contains information which every one can see by their own profile ,like  photos of all your friends in g+
personal tab-tab which can be edited by a person but viewed by everyone , like your profile 

dept tab -tab which can be controlled by people in that dept and other dept coords can only view it 


"""

def display_contacts (request):#this will be a common tab 
    """
    Display all contacts (listed by Department).
    """
    dept_names = [name for name, description in DEP_CHOICES]
    contacts = []
    # Create a list of tuples
    # (Dept Name, List of Core profiles, List of Coord profiles)
    # for each department
    for dept_name in dept_names:
        core_profiles = userprofile.objects.filter (department__Dept_Name = dept_name,
                                                    user__groups__name = 'Cores')
        coord_profiles = userprofile.objects.filter (department__Dept_Name = dept_name,
                                                     user__groups__name = 'Coords')
        contacts.append ((dept_name, core_profiles, coord_profiles))
    for dum in contacts:
	print dum
    return render_to_response('dashboard/display_contacts.html',locals() ,context_instance = global_context(request))



"""
this function creates the directory which will store infromation about the user
like his photos , documents


"""
def create_dir(file_name ,user_name , method=1):
    destdir_one=os.path.join(settings.MEDIA_ROOT,"upload_files")
    destdir=os.path.join(destdir_one,user_name)
    if not os.path.isdir(destdir):
        os.makedirs(destdir,0775)
    save_path=os.path.join(destdir,os.path.basename(file_name))
            
    destdir_one=os.path.join(settings.MEDIA_URL,"upload_files")
    destdir=os.path.join(destdir_one,user_name)
    print destdir , "is the destdir for the file"
    if not os.path.isdir(destdir):
        os.makedirs(destdir,0775)
    file_path=os.path.join(destdir,os.path.basename(file_name))
    
    return (save_path , file_path)



"""
this function writes the file
takes a file and saves it in recpective path


"""
def write_file(save_path ,f ,method=1):
    fout=open(save_path,'wb+')
    for chunk in f.chunks():
        fout.write(chunk)
    fout.close()



    
    
# this function is used for uploading csv files also(for inviting coords)

def upload_invite_coords(request):
    form=InviteForm()
    CsvForm=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"you may write anything here"})
    if request.method=='POST':
        print "post"
        form=UploadFileForm(request.POST,request.FILES)
        if True : #form.is_valid(): yet to check the file            
            file_name=request.FILES['file'].name

            user_name=request.user.username

            save_path ,file_path = create_dir(file_name ,user_name)#passing to the fuction to make directories if not made         
            
            date=datetime.datetime.now()

            try:
                file_present=upload_documents.objects.get(user=request.user,file_name=file_name)
                message="There is a file already with this name .please change the name of the file"
            except:
                f=request.FILES['file']
                write_file(save_path ,f)
		google_path="http://docs.google.com/viewer?url="+file_path
                file_object=upload_documents(user=request.user , file_name=file_name,file_path=file_path,google_doc_path=google_path,url=file_path ,topic="invitation to coords",date=date)#to change topic
                file_object.save()


            message="done"
            """ from here the the csv file is opened and the the coords are invited .yet to be asked and completed """
            
            reader=csv.reader(open(save_path,'rb'),delimiter=' ')
            string=[]
            for field in reader:
                string=string+[field]
            final_string=[]
            for field in string:
        
                splits=field[0].split(';')#; is just temprorary
                final_string=final_string+[splits]
            print final_string
        
        
        else:
            print "the uploadfileform is not valid"

    else:
        pass
        
    return render_to_response('dashboard/invite.html',locals() ,context_instance = global_context(request))




   
        
""" 
personal tab- only request.user can view it
"""
def change_profile_pic(request):
    if request.method == 'POST':
        form=change_pic(request.POST,request.FILES)      
        print "cool"
        if form.is_valid():
            print "form valid"
            file_name="PROFILE_PIC_OF_THE_USER"
            user_name=request.user.username

            save_path ,file_path = create_dir(file_name ,user_name)#passing to the fuction to make directories if not made         
            try:
                photo=userphoto(name =request.user)
            except:
            	pass
            
            f=request.FILES['file']
            write_file(save_path ,f)
	    print save_path
	    if os.path.isfile(save_path):
		print "file path of the user exists "
		delete_object=userphoto.objects.filter(name=request.user)
		delete_object.delete()
	    else :
		print "file path of the user doesnt exists"
            try:
                image_object=userphoto(name=request.user ,photo_path=file_path )
                image_object.save()
                print "photo changed"
            except:
                print "photo not changed"
                pass
	else:
	    print "form not valid"
        return view_profile(request )                
    pic_form=change_pic()
    
    return render_to_response('users/change_profile_pic.html',locals(),context_instance = global_context(request))

#this function is currently not used
def check_perms(owner_name , request):
    if owner_name==None or owner_name==request.user.username:
	upload_message="Your documents and files"
	owner_name=request.user.username	
	user=request.user
	can_delete_files=True
	print user
    else:

	can_delete_files=False
	user=User.objects.get(username=owner_name)
	upload_message=owner_name+" documents and files"	
	print user
	
	return (user ,can_delete_files , upload_message)



""" 
owner  adds a file and views it
other person just views it

"""
@needs_authentication

def upload_file(request ,owner_name=0):
    page_owner = get_page_owner (request, owner_name)
    users_documents=upload_documents.objects.filter(user=page_owner)       
    if request.method=='POST':
        print "post"
        form=UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            print "form is valid"
            file_name=request.FILES['file'].name
            topic=form.cleaned_data['short_description']

	    if topic=="short description of the file":
		topic="No description"

	    print "creating dir for the user "
            save_path ,file_path = create_dir(file_name ,request.user.username)#passing to the fuction to make directories if not made                   
            date=datetime.datetime.now()
            try:
                file_present=upload_documents.objects.get(user=request.user,file_name=file_name)
                message="File with this name exists.please change name  of the file"
            except:
                f=request.FILES['file']
                write_file(save_path ,f)
		google_path="http://docs.google.com/viewer?url="+file_path
                file_object=upload_documents(user=request.user , file_name=file_name,file_path=save_path, url=file_path , google_doc_path=google_path ,topic=topic,date=date)#to change topic
                file_object.save()

            
        else:
            file_name=request.FILES['file'].name


    else:
        print "the user has entered the page not posted (uploaded a doc) :)"
        form=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"short description of the file" ,'file_name':"if left blank , the original name will be used",})

    print "can _edit form views" ,request.session.get('is_visitor','True')
    return render_to_response('dashboard/upload.html',locals() ,context_instance = global_context(request))




"""
personal tab-only user can use it
this function needs lots of changes but one sinle thing isnt working so waiting for that to work ,
"""

@needs_authentication

def delete_file(request,owner_name=None ,number=0 ,file_name="default" ):
    page_owner = get_page_owner (request, owner_name)
    print number ,file_name

    if owner_name==None or owner_name==request.user.username:
	upload_message="Your documents and files"
	owner_name=request.user.username	
	user=request.user
	can_delete_files=True
	print user
    else:

	can_delete_files=False
	user=User.objects.get(username=owner_name)
	upload_message=owner_name+" documents and files"	
	print user
    #user , can_delete_files,upload_message=check_perms(owner_name , request)
    #photo_list=userphoto.objects.filter()


    users_documents=upload_documents.objects.filter(user=page_owner)  
    
    if "d" in request.GET:
        number=request.GET['d']
        print number
        
    if "f" in request.GET:
        file_name=request.GET['f']
        print file_name

        user_name=request.user.username
        destdir_one=os.path.join(settings.MEDIA_ROOT,"upload_files")
        destdir=os.path.join(destdir_one,user_name)
        
        file_path=os.path.join(destdir,os.path.basename(file_name))
        print file_path
        print "harere"
        if os.path.isfile(file_path):
            print "cool"
            os.remove(file_path)
            message=file_name+" deleted"
        else:
            print "file not found"
    try:
        delete_file=upload_documents.objects.get(user=request.user , file_name=file_name)
        delete_file.delete()
    except:
        print "no file"
    photo_list=userphoto.objects.all() 
    form=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"short description of the file"})

    return render_to_response('dashboard/upload.html',locals() ,context_instance = global_context(request))
    

"""
another feature required is by mistake if the user clicks shout two times or refreshes the page,
the comment is passes twice,we can remove it by comparing it with the latest update in the database 

"""


"""
department tab 
vivek thinks we must include AJAX and make this proper and more good
"""
@needs_authentication
def shout(request):
    if request.method=="POST":
        form=shout_box_form(request.POST)
        if form.is_valid():

            print "ya da.."

            time=datetime.datetime.now() 
            comments=form.cleaned_data['comments'] 
	    try:
		last_comment=shout_box.objects.filter(user=request.user).reverse()[0]
		print last_comment
	
            
	    except:
		print "painmax"
            user=userprofile.objects.get(user=request.user)
            try:
		nickname=user.nickname
	    except:
		nickname=request.user.username	
	    try:
		if str(last_comment)!=comments:
                    shout_object=shout_box(user=request.user,nickname=nickname,comments=comments,time_stamp=time)
                    shout_object.save()
            except:    
                shout_object=shout_box(user=request.user,nickname=nickname,comments=comments,time_stamp=time)
                shout_object.save()
                
                
                # chnages done here for ajax integration
    print "shout function here"
    display_dict = dict ()    
    response_dict = {}
    response_dict.update({'name': "it works", 'total': "coming form shout function"})    
    shouts=shout_box.objects.all()
    
    display_dict['shouts']=shouts#by vivek

    print "done"
    """
    return render_to_response('tasks/department_portal.html',simplejson.dumps(response_dict),context_instance = global_context (request))
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')"""
    return display_department_portal(request) 
@needs_authentication


def check_user(request,owner_name ):
    print "the owner id is " ,owner_name
    print "user_is is ",request.user.id
    page_owner=request.user
    if int(owner_name)==int(request.user.id):
        print request.user.id
        print "request,user is viewing the file "
        request.session['is_visitor'] =True
    else:
        print "other person is viewing " ,request.user.id
        try:
            page_owner=User.objects.get(id=owner_name)
        except:
            print "check othercoord view  plaese"
	request.session['is_visitor']=False
    
    
    request.session['page_owner'] = page_owner
    return page_owner


def other_coord(request, owner_name=0):

    
    page_owner=check_user(request,owner_name)
#may be still some stuff is left
	
    return display_portal(request , page_owner.username)

    

