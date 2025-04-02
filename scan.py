from internalLog import writeToInternalLog

class Machine:
    def __init__(self, PT = "", pathToThis = ""):
        self.PT = PT
        self.pathToThis = pathToThis

    def setPTValue (self, PT : str):
        self.PT = PT

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