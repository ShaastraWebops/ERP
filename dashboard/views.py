# -*- coding: utf-8 -*-
"""
Since Django 1.5 drops support for Python 2.5, the json module will be in Python’s standard library,
so django has removed its own copy of simplejson. You can change any use of django.utils.simplejson to json.
import json
using json.dumps() instead of simplejson.dumps()
"""
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.utils.translation import ugettext as _
from django.core.mail import send_mail,EmailMessage
from django.contrib.sessions.models import Session
from erp.dashboard.models import *
from erp.dashboard.forms import *
from erp.department.models import *
from erp.users.models import *
from erp.users.views import view_profile
from erp.users.forms import *
from erp.tasks.views import *
from erp.misc.util import *
from erp.misc.helper import *
from erp.settings import *
import sha,random,datetime,calendar
import os # upload files
from django.conf import settings
from django.utils import simplejson
import csv # invite coords
from create_test_data import *
import time
from django import template
register = template.Library()
import re


"""

Common Tab - a tab which contains information which every one can see by their own profile ,like  photos of all your friends in g+
personal tab-tab which can be edited by a person but viewed by everyone , like your profile 

dept tab -tab which can be controlled by people in that dept and other dept coords can only view it 


"""
@needs_authentication
def display_contacts (request , owner_name=None):#this will be a common tab 
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

        dept_name_underscore = re.sub('[^a-zA-Z0-9]', '_', dept_name)

        contacts.append ((dept_name, core_profiles, coord_profiles, dept_name_underscore))

    #Get Department Members' image thumbnails
    display_dict = dict ()
    page_owner = get_page_owner (request, owner_name=None)
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_supercoords_list = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

    for dum in contacts:
	print dum
	curr_user=request.user

    return render_to_response('dashboard/display_contacts.html',locals() ,context_instance = global_context(request))




    
    
# this function is used for uploading csv files also(for inviting coords)
@needs_authentication
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
@needs_authentication
def change_profile_pic(request, owner_name):
    print request.user , "in change-profile-pic"
    if request.method == 'POST':
        form=change_pic(request.POST,request.FILES)      
        if form.is_valid():
            print "change pic form valid"
            file_name="PROFILE_PIC_OF_THE_USER.jpg"
            user_name=request.user.username
            try:
                supercores = request.user.get_profile().department.owner.all()
                supercore = supercores[0]
                for x in supercores:
                    if request.user.username.startswith(x.username.lower()):
                        supercore = x
                        break
                
                if request.user.username.startswith(supercore.username.lower()):
                    departments = supercore.department_set.all()
                    for dept in departments:
                        allUserProfiles = userprofile.objects.filter(department = dept)
                        for each in allUserProfiles:
                            if each.user.username.startswith(supercore.username.lower()):
                                save_path, file_path = create_dir(file_name, each.user.username)#passing to the fuction to make directories if not made
                                try:
                                    photo=userphoto(name = each.user)
                                except:
                                	pass
                                f=request.FILES['file']
                                write_file(save_path ,f)
                                print save_path
                                if os.path.isfile(save_path):
                                    print "file path of the user photo exists"
                                    delete_object=userphoto.objects.filter(name=each.user)
                                    delete_object.delete()
                                else :
                                    print "file path of the user photo doesnt exists"
                                try:
                                    image_object=userphoto(name=each.user, photo_path=file_path )
                                    image_object.save()
                                    print "profile photo changed"
                                except:
                                    print "profile photo not changed"
                                    pass                                       

                else:                                                            #there may be an account in a department having a supercore, but is not a supercore-associated account. 
                    department = request.user.get_profile().department

                    if request.user.username.endswith(re.sub('[^a-zA-Z0-9]', '', department.Dept_Name).lower()):                #a multiple coord-associated acc.  

                        allUserProfiles = userprofile.objects.all()
                        multiple_coord=request.user.username.split('_')[0]
                        for each in allUserProfiles:
                            if (each.user.username.startswith(multiple_coord.lower()) and each.user.username.lower()!=multiple_coord.lower()):
                                save_path, file_path = create_dir(file_name, each.user.username)#passing to the fuction to make directories if not made
                                try:
                                    photo=userphoto(name = each.user)
                                except:
                                  	pass
                                f=request.FILES['file']
                                write_file(save_path ,f)
                                print save_path
                                if os.path.isfile(save_path):
                                    print "file path of the user photo exists"
                                    delete_object=userphoto.objects.filter(name=each.user)
                                    delete_object.delete()
                                else :
                                    print "file path of the user photo doesnt exists"
                                try:
                                    image_object=userphoto(name=each.user, photo_path=file_path )
                                    image_object.save()
                                    print "profile photo changed"
                                except:
                                    print "profile photo not changed"
                                    pass
                    else:                        
                        file_name="PROFILE_PIC_OF_THE_USER.jpg"
                        user_name=request.user.username
                        save_path ,file_path = create_dir(file_name ,user_name)#passing to the fuction to make directories if not made       
                    
                        try:
                            photo=userphoto(name = request.user)
                        except:
                            pass
                        f=request.FILES['file']
                        write_file(save_path ,f)      
                        print save_path
                        if os.path.isfile(save_path):
                            print "file path of the user photo exists"
                            delete_object=userphoto.objects.filter(name=request.user)
                            delete_object.delete()
                        else :
                            print "file path of the user photo doesnt exists"
                        try:
                            image_object=userphoto(name=request.user, photo_path=file_path )
                            image_object.save()
                            print "profile photo changed"
                        except:
                            print "profile photo not changed"
                            pass
                        
            except:
                department = request.user.get_profile().department                              #multiple-coord-associated acc, in a dept without a supercore.

                if request.user.username.endswith(re.sub('[^a-zA-Z0-9]', '', department.Dept_Name).lower()):           #a multiple coord-associated acc.  
                    allUserProfiles = userprofile.objects.all()
                    multiple_coord=request.user.username.split('_')[0]
                    for each in allUserProfiles:
                        if (each.user.username.startswith(multiple_coord.lower()) and each.user.username.lower()!=multiple_coord.lower()):
                            save_path, file_path = create_dir(file_name, each.user.username)#passing to the fuction to make directories if not made
                            try:
                                photo=userphoto(name = each.user)
                            except:
                              	pass
                            f=request.FILES['file']
                            write_file(save_path ,f)
                            print save_path
                            if os.path.isfile(save_path):
                                print "file path of the user photo exists"
                                delete_object=userphoto.objects.filter(name=each.user)
                                delete_object.delete()
                            else :
                                print "file path of the user photo doesnt exists"
                            try:
                                image_object=userphoto(name=each.user, photo_path=file_path )
                                image_object.save()
                                print "profile photo changed"
                            except:
                                print "profile photo not changed"
                                pass
                
                else:
                    file_name="PROFILE_PIC_OF_THE_USER.jpg"
                    user_name=request.user.username
                    save_path ,file_path = create_dir(file_name ,user_name)#passing to the fuction to make directories if not made       
                    
                    try:
                        photo=userphoto(name = request.user)
                    except:
                   	    pass
                    f=request.FILES['file']
                    write_file(save_path ,f)      
                    print save_path
                    if os.path.isfile(save_path):
                        print "file path of the user photo exists"
                        delete_object=userphoto.objects.filter(name=request.user)
                        delete_object.delete()
                    else:
                        print "file path of the user photo doesnt exists"
                    try:
                        image_object=userphoto(name=request.user, photo_path=file_path )
                        image_object.save()
                        print "profile photo changed"
                    except:
                        print "profile photo not changed"
                        pass
        else:
            print "form not valid"

        return redirect ('erp.users.views.handle_profile', owner_name = request.user.username)

    pic_form=change_pic()

    #Get Department Members' image thumbnails
    page_owner = get_page_owner (request, owner_name=None)
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_supercoords_list = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)



    
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
def upload_file(request ,owner_name=None):
    page_owner = get_page_owner (request, owner_name)
    users_documents=upload_documents.objects.filter(user=page_owner)       
    if request.method=='POST':
        print "post"
        form=UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            print "form is valid"
            file_name=request.FILES['file'].name
            title=form.cleaned_data['title']
            topic=form.cleaned_data['short_description']

        if (topic=="short description of the file"):
            topic="No description"

        try:
            extension = file_name.split('.')[-1]
        except:
            extension=''
            
	    print "creating dir for the user "
            save_path ,file_path = create_dir(file_name ,request.user.username)#passing to the fuction to make directories if not made                   
            date=datetime.datetime.now()
            try:
                file_present=upload_documents.objects.get(user=request.user,file_name=file_name)
                try:
                    file_present=upload_documents.objects.get(user=request.user,file_name=(title+extension))
                    message="File with this name exists.please change name  of the file"
                except:
                    save_path ,file_path = create_dir((title+extension) ,request.user.username)#passing to the fuction to make directories if not made
                    f=request.FILES['file']
                    write_file(save_path ,f)
                    google_path="http://docs.google.com/viewer?url="+file_path
                    file_object=upload_documents(user=request.user , file_name=(title+extension),file_path=save_path, url=file_path , google_doc_path=google_path ,topic=topic,date=date,title=title)#to change topic
                    file_object.save()
            except:
                f=request.FILES['file']
                write_file(save_path ,f)
                google_path="http://docs.google.com/viewer?url="+file_path
                file_object=upload_documents(user=request.user , file_name=file_name,file_path=save_path, url=file_path , google_doc_path=google_path ,topic=topic,date=date,title=title)#to change topic
                file_object.save()

    form=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"short description of the file" ,'file_name':"if left blank , the original name will be used",})

    print "can _edit form views" ,request.session.get('is_visitor','True')
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    
    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_supercoords_list = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)


    return render_to_response('dashboard/upload.html',locals() ,context_instance = global_context(request))




"""
personal tab-only user can use it
this function needs lots of changes but one sinle thing isnt working so waiting for that to work ,
"""

@needs_authentication
def delete_file(request,owner_name=None ,number=0  ):
    page_owner = get_page_owner (request, owner_name)
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)    
    users_documents=upload_documents.objects.filter(user=page_owner)    
    form=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"short description of the file"})   
    try:
        user_name=request.user.username
        file_to_be_deleted=upload_documents.objects.get(id=number)
        print "the path of the file to be delete is  :" ,file_to_be_deleted
        file_name=file_to_be_deleted.file_name
        if os.path.isfile(str(file_to_be_deleted)):
            os.remove(str(file_to_be_deleted))
            message=file_name+" deleted"
        else:
            print "file not found"
        print file_name , "the file name "
        delete_file=upload_documents.objects.get(user=request.user , file_name=file_name)
        delete_file.delete()
    except:
        print "no file"
         
        
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



def test(request):
    print "in test function"
    return render_to_response('dashboard/dummy.html',{})

@register.filter
def epoch(value):
    try:
        return int(time.mktime(value.timetuple())*1000)
    except AttributeError:
        return ''  

@needs_authentication
def display_calendar(request ,owner_name=None , month=0 ,year=0):
    page_owner=get_page_owner(request ,owner_name=owner_name)
    if is_core(page_owner):
        user_tasks=Task.objects.filter(creator = page_owner)
    else:
        user_tasks=SubTask.objects.filter(coords=page_owner.id)
    
    complete_data=[]
    if is_core(page_owner):
        for sub in user_tasks:
            creation_date=str(sub.creation_date).split(' ')[0]
            complete_data.append({"title": str(sub.subject), "type": "task", "url": "../../display_task/" + str(sub.id), "date": str(epoch(sub.deadline)), "description": str(sub.status)})
    else:
        for sub in user_tasks:
            creation_date=str(sub.creation_date).split(' ')[0]
            complete_data.append({"title": str(sub.subject), "type": "subtask", "url": "../../subtask/" + str(sub.id), "date": str(epoch(sub.deadline)), "description": str(sub.status)})
    
    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_supercoords_list = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)
    
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)    


    return render_to_response('dashboard/mycalendar.html',locals() ,context_instance = global_context(request))
  
    

def load_data(request):
    do_it_all()
    return render_to_response('gen.html',locals())
