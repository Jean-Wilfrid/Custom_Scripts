from internalLog import writeToInternalLog

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