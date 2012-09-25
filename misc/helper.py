from django.contrib.auth.models import User
import sha,random,datetime
from django.core.mail import send_mail,EmailMessage,get_connection
from django.template.loader import get_template
from django.template.context import Context, RequestContext
import os
from shutil import copyfile
from django.conf import settings
from erp.users.models import *
from erp.dashboard.models import *

def is_multiple_user (user):
    """
    Return True if the user is Core of multiple depts
    """
    try:
        if (user.get_profile().department.all()[0]):
            return False
    except:
        pass
    return True

def is_core (user):
    """
    Return True if user is a Core.
    """
    if user.groups.filter (name = 'Cores'):
        return True
    return False

def is_supercoord (user):
    """
    Return True if user is a Supercoord.
    """
    if user.groups.filter (name = 'Supercoords'):
        return True
    return False

def is_coord (user):
    """
    Return True if user is a Coord.
    """
    if user.groups.filter (name = 'Coords'):
        return True
    return False

def get_page_owner (request, owner_name):
    """
    If owner_name is passed, return page owner, if he exists. If user
    with that name doesn't exist, return 'Invalid'.

    Else, return current user.

    Also, set the session variable for page_owner.
    """
    print 'Get Page Owner - owner_name : ', owner_name
    if owner_name == '' or owner_name is None:
        page_owner = request.user
    else:
        try:
            page_owner = User.objects.get (username = owner_name)
        except:
            return 'Invalid'
    request.session['page_owner'] = page_owner
    return page_owner
    
def get_department(request):
    try:
        print request.user
        return userprofile.objects.get(user = request.user).department.all()[0].Dept_Name
    except:
        return None

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
    
    print destdir            
    destdir_one=os.path.join(settings.MEDIA_URL,"upload_files")
    destdir=os.path.join(destdir_one,user_name)
    print destdir , "is the destdir for the file"
    file_path=os.path.join(destdir,os.path.basename(file_name))
    
    return (save_path , file_path)

def check_dir(user):
    """
    Checks whether the user has a upload folder for himself.
    """
    destdir_one=os.path.join(settings.MEDIA_ROOT,"upload_files")
    destdir=os.path.join(destdir_one, user.username)
    if not os.path.isdir(destdir):
        os.makedirs(destdir,0775)
    src=os.path.join(settings.MEDIA_ROOT,"images")
    src=os.path.join(src,os.path.basename("default.jpeg"))
    dest=os.path.join(destdir,os.path.basename("PROFILE_PIC_OF_THE_USER.jpg"))
    copyfile(src, dest)
    dest=os.path.join(settings.MEDIA_URL,"upload_files")
    dest=os.path.join(dest, user.username)
    dest=os.path.join(dest,os.path.basename("PROFILE_PIC_OF_THE_USER.jpg"))
    print dest
    image_object=userphoto(name=user, photo_path=dest)
    image_object.save()
    google_path="http://docs.google.com/viewer?url="+dest
    topic="Profile picture of the user."
    date=datetime.datetime.now()
    title=user.get_profile().name+"'s Profile Picture."
    file_object=upload_documents(user=user , file_name="PROFILE_PIC_OF_THE_USER.jpg", file_path=dest, url=dest , google_doc_path=google_path ,topic=topic,date=date,title=title)
    file_object.save()    

"""
this function writes the file
takes a file and saves it in recpective path


"""

def write_file(save_path ,f ,method=1):
    fout=open(save_path,'wb+')
    for chunk in f.chunks():
        fout.write(chunk)
    fout.close()
    
"""
helper function to mail junta
using it for invitation and forgot password thing

"""
def mail_coord(hyperlink ,mail_header ,name ,template,mail , password=""):
    print "mail helper function here hey"
    mail_template=get_template(template)
    print mail_template
    salt = sha.new(str(random.random())).hexdigest()[:5]
    activation_key = sha.new(salt+name).hexdigest()
    print activation_key
    body=mail_template.render(Context({'coordname':name,
                                                   'SITE_URL':hyperlink,
                                                   'activationkey':activation_key,
                                                   'new_password':password
                                                   }))
    send_mail(mail_header,body,'noreply@shaastra.org',mail,fail_silently=False)
    success_message="mail sent"
    return success_message

