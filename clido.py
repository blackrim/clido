import argparse
from datetime import datetime
import operator
import hashlib
import sys,os

"""
CLASSES
"""
class TColors:
    CYAN = '\033[36m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    WHITE = '\33[37m'
    ENDC = '\033[39m'

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
    def __init__(self,_id,description,date):
        self._id = _id
        self.description = description
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
        mainpath = os.path.join(os.path.expanduser(self.maindir),self.label)
        mainpath_del = os.path.join(os.path.expanduser(self.maindir),self.label+".del")
        if create:
            if os.path.exists(mainpath) and os.path.exists(mainpath_del):
                raise TDFilesExist
            fl = open(mainpath,"w")
            fl.close()
            fl = open(mainpath_del,"w")
            fl.close()
        else:
            if os.path.exists(mainpath) and os.path.exists(mainpath_del):
                #need to read the items in the list
                fl = open(mainpath,"r")
                for i in fl:
                    spls = i.strip().split("||")
                    if len(spls) > 0:
                        td = TD(spls[0],spls[1],spls[2])
                        self.tds[spls[0]] = td 
                fl.close()
                fl = open(mainpath_del,"r")
                for i in fl:
                    spls = i.strip().split("||")
                    if len(spls) > 0:
                        td = TD(spls[0],spls[1],spls[2])
                        self.del_tds[spls[0]] = td 
                fl.close()
                return
            else:
                raise TDFilesNotFound

    def get_tdid(self,_idstart):
        """
        given the starting text, we try and get the task
        """
        match = filter(lambda _id: _id.startswith(_idstart),self.tds.keys())
        if len(match) == 1:
            return match[0]
        elif len(match) == 0:
            return
        else:
            return

    def add_td(self,description):
        dt = datetime.now()
        td = TD(create_hash(description),description,str(dt))
        self.tds[td._id] = td
        return

    def del_td(self,_idstart):
        match = self.get_tdid(_idstart)
        self.del_tds[match] = self.tds[match]
        del self.tds[match]
        return

    def write_tds(self):
        mainpath = os.path.join(os.path.expanduser(self.maindir),self.label)
        mainpath_del = os.path.join(os.path.expanduser(self.maindir),self.label+".del")
        fl = open(mainpath,"w")
        for i in self.tds:
            fl.write(i+"||"+self.tds[i].description+"||"+self.tds[i].date+"\n")
        fl.close()
        fl = open(mainpath_del,"w")
        for i in self.del_tds:
            fl.write(i+"||"+self.del_tds[i].description+"||"+self.del_tds[i].date+"\n")
        fl.close()
        return

    def list_tds(self):
        tdsds = {}
        for i in self.tds:
            tdsds[i] = self.tds[i].date
        sorted_d = sorted(tdsds.iteritems(), key=operator.itemgetter(1),reverse=False)
        for i in sorted_d:
            print TColors.GREEN+i[0][0:5]+TColors.ENDC,TColors.CYAN+self.tds[i[0]].date+TColors.ENDC,TColors.RED+self.tds[i[0]].description+TColors.ENDC
        return


"""
FUNCTIONS
"""
def create_hash(text):
    return hashlib.sha1(text).hexdigest()

#add
#   list the lists
#   unique for not just description?
def construct_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--folder",help="main directory",required=True)
    parser.add_argument("-l","--list",help="the list",required=True)
    parser.add_argument("-d","--delete",help="delete an item")
    parser.add_argument("-e","--edit",help="edit an item",nargs="+")
    parser.add_argument("-a","--add",help="add an item",nargs="+")
    parser.add_argument("-s","--show",help="show all the items in a list",action="store_true")
    parser.add_argument("-m","--makelist",help="create a list",action="store_true")
    return parser

if __name__ == "__main__":
    args = construct_parser().parse_args()
    if args.makelist:
        tdl = TDList(args.folder,args.list,create=True)
        sys.exit(0)
    #not creating a list so doing something else
    tdl = TDList(args.folder,args.list,create=False)
    if args.add:
        text = " ".join(args.add)
        tdl.add_td(text)
    elif args.delete:
        tdl.del_td(args.delete)
    elif args.show:
        tdl.list_tds()
    tdl.write_tds()
