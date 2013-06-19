import os.path
import shutil
import errno

def mkdir_p(path):
    """
    http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python 
    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def copy_content(dir, src, refresh=False, name=None):
    """
    dir : string
        The first subdirectory of content. 'notebooks', 'images', etc
    src : string
        filepath. If absolute, this will copy to local content dir. If local, will assume path
        within content. 
        src may also have a special name: prefix that will translate to content/{dir}/{name}
        similar to the name param
    refresh : boolean
        Regrab the src notebook and place it into content/notebooks. Otherwise, only 
        replace if content copy does not exist
    name : string
        Overrides name. This is so we can be sure to lockin a copy and not have it
        overwritten by another Article that references the same notebook. Anchored to
        content/{dir}
    """
    content_dir = os.path.join('content', dir)

    # special name prefix is anchored to content/{dir}
    prefix = 'name:'
    if src.startswith(prefix):
        src = src[len(prefix):]
        src = os.path.join(content_dir, src)

    # first assume local file
    nb_path = src
    dirpath = os.path.dirname(src)

    if os.path.isabs(src): # non local
        # only build out the first two parent directories
        sdir, filename = os.path.split(src)
        sdirs = sdir.split('/')[-2:]

        if name:
            filename = name
            sdirs = []

        dirpath = os.path.join('content', dir, '/'.join(sdirs))
        nb_path = os.path.join(dirpath, filename)
    

    # already have local copy. move along
    if not refresh and os.path.isfile(nb_path):
        return nb_path

    if not os.path.exists(src):
        raise ValueError("File {0} could not be found".format(src))

    if src != nb_path:
        # copy file over
        mkdir_p(dirpath)
        shutil.copyfile(src, nb_path)
    return nb_path
