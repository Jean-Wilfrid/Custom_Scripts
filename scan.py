import internalLog as il
import formatChecker as fc
import os
class Machine ():
    def __init__(self, PT = "", pathToThis = ""):
        self.PT = PT
        self.pathToThis = pathToThis

    def setPTValue (self, PT : str):
        self.PT = PT #The use of capital letters is necessary to distinguish the attributes of these classes and the local variables of functions of other modules manipulating this set of data. 

    def setPathToThisValue (self, pathToThis : str):
        self.pathToThis = pathToThis

class Project ():
    def __init__(self, OTP : str = "", machines : list[Machine] = []):
        self.OTP = OTP
        self.machines = machines

    def setOTPValue(self, OTP : str = ""):
        self.OTP = OTP

    def addMachine(self, machine : Machine):
        self.machines.append(machine)

class PFH10Repairs():
    def __init__(self, projects : list[Project] = []):
        self.projects = projects

    def addProject(self, project : Project):
        self.projects.append(project)

def getProjectsList(path : str) -> list:#Take a path and return a list of project name in that folder
    obj = os.scandir(path)
    plist = []
    for entry in obj:
        temp = entry.name.split()
        if fc.rightOTPFormat(temp[0]):
            plist.append(temp)
    return plist

def getMachinesList(path : str) -> list[Machine]:#Scan a project directory and returns the list of machines inside
    obj = os.scandir(path)
    mlist = []
    for entry in obj:
        if entry.is_dir() and fc.rightPTFormat(entry.name.split()[-1]):
            machine = Machine()
            machine.setPTValue(entry.name.split()[-1])
            machine.setPathToThisValue(entry.path)
            mlist.append(machine)
    return mlist

def linkMachinesToProject(path : str, elt : str) -> Project:#Take a project's name and its parent path. Returns a project object set up.
    project = Project()
    project.setOTPValue(getOTP(elt))
    mPath = os.path.join(path,elt)
    mlist = getMachinesList(mPath)
    for m in mlist:
        project.addMachine(m)
    return project

def joinNames(plist : list[list[str]]) -> list[str]:#Take a list of lists of strings and join each list of strings into a string
    jlist = []
    for elt in plist:
        elt = " ".join(elt)
        jlist.append(elt)
    return jlist

def getOTP(name : str) -> str:#name is assume to be a project directory name. Then the function returns its OTP
    a = name.split()
    return a[0]

def scan(path : str):#Scan the path 
    repairs = PFH10Repairs()

    slist = getProjectsList(path)
    slist = joinNames(slist)

    for elt in slist :
        project = linkMachinesToProject(path,elt)
        repairs.addProject(project)
    
    return repairs

a = r"C:\Home\PREE\Test"
#elt = "IS0-800442 - DOEL"
#a = input("Entrer chemin :")
#a = fc.toRaw(a)
#b = linkMachinesToProject(a,elt)
b = scan(a)

for p in b.projects:
    print(p.OTP)
    for m in p.machines:
        print(m.PT)
