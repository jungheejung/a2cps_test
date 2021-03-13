import os, pydicom, shutil

def make_copy(path):
    """
    Makes a copy of the original data. The original data is saved with a suffix "_orig"
    """
    suffix = '-orig'
    dst = os.path.join(path+suffix)
    print("Making a copy of the data...")
    if os.path.isdir(dst):
        flag=True
        print("Destination directory already exists")
    else:
        shutil.copytree(path, dst)
        flag=False
        print("Done!The original copy is %s"%dst)
    return path,flag

def get_subdirectory(path):
    """
    Returns all the subdirectories under 'func' directory of the raw subject data.
    """
    dirs = []
    for dirpath, dirnames, filenames in os.walk(path):
        if not dirnames:
            dirs.append(dirpath)
    return dirs

def delete_trigger_tag(filepath):
    """
    Deletes the trigger tag (0018,1060) from the DICOM file.
    """
    # Copy the data, add suffix "_orig" to the original data and return the path of duplicate data
    new_path,_  = make_copy(filepath)

    dirs = get_subdirectory(filepath)

    for func in dirs:
        print("Deleting tag for %s"%func)
        for i in sorted(os.listdir(func)):
            ds = pydicom.read_file(os.path.join(func,i))
            try:
                # Only fMRI images will have the tag
                # Delete the dicom tag 0018,1060. This tag represents the Trigger value
                del(ds['0018','1060'])
                # save the edited dicom file in the same directory
                ds.save_as(os.path.join(func,i))
            except:
                print("Skipping! Dicoms in %s do not have trigger tag..."%os.path.join(func))
                break
    print("Done!")
