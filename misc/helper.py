from django.contrib.auth.models import User
import sha,random,datetime
from django.core.mail import send_mail,EmailMessage,SMTPConnection
from django.template.loader import get_template
from django.template.context import Context, RequestContext
import os
from shutil import copyfile
from django.conf import settings
from erp.users.models import userphoto

# Temporary workaround for the fact that I don't know whether / how to
# extend the User class with methods
def is_core (user):
    """
    Return True if user is a Core.
    """
    if user.groups.filter (name = 'Cores'):
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

def check_dir(request):
    """
    Checks whether the user has a upload folder for himself.
    """
    destdir_one=os.path.join(settings.MEDIA_ROOT,"upload_files")
    destdir=os.path.join(destdir_one, request.user.username)
    if not os.path.isdir(destdir):
        os.makedirs(destdir,0775)
        src=os.path.join(settings.MEDIA_ROOT,"images")
        src=os.path.join(src,os.path.basename("default.jpeg"))
        dest=os.path.join(destdir,os.path.basename("PROFILE_PIC_OF_THE_USER"))
        copyfile(src, dest)
        dest=os.path.join(settings.MEDIA_URL,"upload_files")
        dest=os.path.join(dest, request.user.username)
        dest=os.path.join(dest,os.path.basename("PROFILE_PIC_OF_THE_USER"))
        image_object=userphoto(name=request.user, photo_path=dest)
        image_object.save()

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

