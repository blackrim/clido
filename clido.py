import argparse
import datetime
import hashlib
import sys,os

"""
CLASSES
"""
class TDFilesNotFound(Exception):
    def __init__(self):
        print "files not found"
        sys.exit(0)

class TDFilesExist(Exception):
    def __init__(self):
        print "files already exist"
        sys.exit(0)

class TD:
    """
    this is a particular todo
    """
    def __init__(self,_id,date):
        self._id = _id
        self.date = date


class TDList:
    """
    a todo list set. this will include both the ones left todo as well
    as those that have been deleted.

    maindir - where the files are listed
    label - the name of this particular list
    """
    def __init__(self,maindir,label,create=False):
        self.tds = {} #the unfinished todos
        self.del_tds = {} #the finished todos
        self.maindir = maindir
        self.label = label
        mainpath = os.path.join(os.path.expanduser(self.maindir),label)
        mainpath_del = os.path.join(os.path.expanduser(self.maindir),label+".del")
        if create:
            if os.path.exists(mainpath) and os.path.exists(mainpath_del):
                raise TDFilesExist
            fl = open(mainpath,"w")
            fl.close()
            fl = open(mainpath_del,"w")
            fl.close()
        else:
            if os.path.exists(mainpath) and os.path.exists(mainpath_del):
                return
            else:
                raise TDFilesNotFound

"""
FUNCTIONS
"""
def create_hash(text):
    return hashlib.sha1(text).hexdigest()

def construct_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--folder",help="main directory",required=True)
    parser.add_argument("-l","--list",help="the list",required=True)
    parser.add_argument("-d","--delete",help="delete an item")
    parser.add_argument("-e","--edit",help="edit an item")
    parser.add_argument("-a","--add",help="add an item")
    parser.add_argument("-m","--makelist",help="create a list",action="store_true")
    return parser

if __name__ == "__main__":
    args = construct_parser().parse_args()
    print args
    if args.makelist:
        tdl = TDList(args.folder,args.list,create=True)
        sys.exit(0)
    if args.delete:
        print "delete"
