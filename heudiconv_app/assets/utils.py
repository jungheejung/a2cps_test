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
    new_path,flag  = make_copy(filepath)

    if not flag:
        # Only fMRI images will have the tag. Selecting all the sub-directories of 'func'  directory
        fmri_image_path = os.path.join(new_path,'func')
        dirs = get_subdirectory(fmri_image_path)

        for func in dirs:
            print("Deleting tag for %s"%func)
            for i in sorted(os.listdir(func)):
                ds = pydicom.read_file(os.path.join(func,i))
                # Delete the dicom tag 0018,1060. This tag represents the Trigger value
                del(ds['0018','1060'])
                # save the edited dicom file in the same directory
                ds.save_as(os.path.join(func,i))
            print("Done! New dicoms are stored in %s"%os.path.join(func))
    else:
        print("Skipping!")
