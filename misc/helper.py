from django.contrib.auth.models import User

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
