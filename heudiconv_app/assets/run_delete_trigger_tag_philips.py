import sys
from utils import delete_trigger_tag
try:
    inputfile = sys.argv[1]
    print("Deleting Trigger tag for %s "%inputfile)
    delete_trigger_tag(inputfile)
except:
    raise ValueError("Please specify the full path of the raw subject data directory")
