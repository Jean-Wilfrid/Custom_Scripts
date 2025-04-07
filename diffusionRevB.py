import os
import scan as sc
import internalLog as il
import formatChecker as fc

def thereIsOnlyDirs(subPath : str) -> bool: # Check if there is only directories in this folder
    obj = os.scandir(subPath) #Scan the dir and get iterable object
    so = True
    for entry in obj:
        if entry.is_file() or entry.is_symlink(): #Break the loop at the first occurence of a symlink or file
            so = False
            break

    return so

def getCERName(parentPath : str) -> list[str]:
    obj = os.scandir(parentPath)

    rawName = ""
    for entry in obj:
        if entry.name.startswith("CER_B") or entry.name.startswith("CER"): #Find the file with the name starting with either options 
            rawName = entry.name.split() #Split to isolate the last block for further use
            break
    
    return rawName

def removeExtension(rawName : list[str]) -> list[str]:
    try:
        buffer = rawName[-1].split(".") #Seperate the last part of the name and the extension name
    except IndexError: #This is certainly due to an emtpy string
        msg = "Il n'y a pas de fichier commençant par 'CER' ou 'CER_B'. Une chaîne vide continue le process.\n"
        il.writeToInternalLog(msg)
        return rawName

    del rawName[-1] #Delete the whole block
    rawName.append(buffer[0]) #Get back last part without the extension name in the main list
    return rawName

def getIDNumber(buffer : str) -> tuple[str,int]:
    try: #In this case the filename begin with CER followed by a space i.e CER 24-10
        nums = buffer[1].split("-")
        num = int (nums[1])
        i = 2 #This is the index of the first part of the machine's name. Its value change according to name's beginning
    except IndexError: #In this one, the file's name begin with CER followed by the id number with no space i.e CER24-10
        try:
            nums = buffer[0].split("-") 
            num = int (nums[1])
            i = 1 #This is the index of the first part of the machine's name its value change according to name's beginning
        except IndexError:
            msg = "Le format du nom du fichier CER ne permet pas la création du dossier.\n"
            il.writeToInternalLog(msg)
            return "", i

    if num < 10 : #Adding a 0 at the beginnig to keep the naming style
        num = "0" + str(num)
    else:
        num = str(num)
    
    return num, i

def getMachinesName(buffer :str, i : int) -> str:
    name = ""
    try:
        index = 1
        while index : #delete all "-"
            index = buffer.index("-")
            del buffer[index]
    except ValueError: #It means that there is no "-" used in the filename except in the OTP
        index = len(buffer) - 1
        while i < index - 1 : #Merging all the parts in a single name
            name += buffer[i]
            name += " "
            i += 1
        name += buffer[index - 1]

    return name


def createTargetDirectoryName(buffer : list[str]) -> str: 

    #Getting id number
    num,i = getIDNumber(buffer)

    #Getting OTP
    otp = buffer[-1]
    if not fc.rightOTPFormat(otp):
        otp = ""

    #Getting machine's name
    name = getMachinesName(buffer, i)

    #Final Line Merging
    if num =="" or otp == "" or name =="": #If there is any error, the line is set to empty
        finalLine = ""
    else:
        finalLine = num + " " + otp + " " + name

    return finalLine

def createTargetDirectory (sourcePath : str, targetPath : str) -> str:

    dirName = getCERName(sourcePath)
    dirName = removeExtension(dirName)
    if dirName == "":
        msg = f'La chaîne de caractères reçue ne permet pas de créer le dossier CER lié à : "{sourcePath}".\n'
        il.writeToInternalLog(msg)
        return ""
    dirName = createTargetDirectoryName(dirName)
    if dirName == "":
        msg = f'La chaîne de caractères reçue ne permet pas de créer le dossier CER lié à : "{sourcePath}".\n'
        il.writeToInternalLog(msg)
        return ""
    finalPath = os.path.join(targetPath,dirName)

    try:
        os.makedirs(finalPath, exist_ok=True)
    except OSError:
        print ("Le dossier " + finalPath + " ne peut être crée")

    return finalPath

def copyFilesToPoleReg(sourcePath : str, targetPath : str):
    obj = os.scandir(sourcePath)
    if thereIsOnlyDirs(sourcePath):
        for entry in obj: #Iterate until you get inside the machine's directory containing both files and directories
            newSourcePath = os.path.join(sourcePath, entry.name)
            copyFilesToPoleReg(newSourcePath, targetPath)
    else:
        target = createTargetDirectory(sourcePath, targetPath)
        if target == "":
            pass
        else:
            command = f'robocopy "{sourcePath}" "{target}" /E /COPY:DATSO /DCOPY:DATE /MT[:16] /UNILOG+:output.txt /ETA /TEE'  #See help robocopy in a cmd to get more details
            os.system(command)


def getOTPandPT(buffer :  list[str]) -> tuple[str, str]:
    #Getting OTP
    otp = buffer[-1]
    if not fc.rightOTPFormat(otp):
        otp = ""
        msg = f'L\'OTP n\'est pas au bon format.\n'
        il.writeToInternalLog(msg)

    #Getting PT
    pt = ""
    try:
        index = 1
        while index : #delete all "-"
            index = buffer.index("-")
            del buffer[index]
    except ValueError: #It means that there is no "-" used in the filename except in the OTP
        pt = buffer[-2]
        if not fc.rightPTFormat(pt):
            pt = ""
            msg = f'Le n° de PT n\'est pas au bon format.\n'
            il.writeToInternalLog(msg)

    return otp, pt

def findTargetDirectory(buffer : list[str], targetPath : str, endPart : str) -> str:
    otp, pt = getOTPandPT(buffer)
    if otp == "" or pt == "":
        msg = f'La sélection du dossier cible n\'est pas possible.\nVérifier le format de {buffer}.pdf\n'
        il.writeToInternalLog(msg)
        return ""
    repairs = sc.scan(targetPath)
    for elt in repairs.projects:
        if otp == elt.OTP:
            for item in elt.machines :
                if pt == item.PT:
                    target = os.path.join(item.pathToThis, endPart)
                    return target
            msg = f'Le n° {pt} correspondant à {otp} n\'a pas été trouvé.\n'
            il.writeToInternalLog(msg) 
            return ""
    msg = f'L\'OTP : {otp} n\'a pas été trouvé.\n'
    il.writeToInternalLog(msg) 
    return ""

def selectTargetDirectory(sourcePath : str, targetPath : str, endPart : str) -> str:
    dirName = getCERName(sourcePath)
    dirName = removeExtension(dirName)
    if dirName == "":
        msg = f'La chaîne de caractères reçue ne permet pas de trouver le dossier CER lié à : "{sourcePath}".\n'
        il.writeToInternalLog(msg)
        return ""
    target = findTargetDirectory(dirName, targetPath, endPart)
    if target == "":
        msg = f'La copie n\'est pas possible vers : "{targetPath}".\n'
        il.writeToInternalLog(msg)
    return target


def copyFilesToPFH10(sourcePath : str, targetPath : str, endPart :str):
    obj = os.scandir(sourcePath)
    if thereIsOnlyDirs(sourcePath):
        for entry in obj: #Iterate until you get inside the machine's directory containing both files and directories
            newSourcePath = os.path.join(sourcePath, entry.name)
            copyFilesToPFH10(newSourcePath, targetPath, endPart)
    else:
        target = selectTargetDirectory(sourcePath, targetPath, endPart)
        if target == "":
            pass
        else:
            command = f'robocopy "{sourcePath}" "{target}" CER* /COPY:DATSO /UNILOG+:output.txt /ETA /TEE'  #See help robocopy in a cmd to get more details
            os.system(command)
