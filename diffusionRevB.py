import os
from internalLog import writeToInternalLog

homePath = r"C:\Users\jt30320l\Box\y_POLE REGULATION\01 - Suivi PFH\8 - Partage CER\CER\Attente validation client"
poleRegCERPath = r"C:\Users\jt30320l\Box\y_POLE REGULATION\01 - Suivi PFH\2 - Expertise\Z_EXPERTISE 2024" #Try to automate the choice of this folder later
pfh10RepairsPath = r"C:\Users\jt30320l\Box\Plateforme Hydraulique - GAIA\PFH10-SDP interservices\REPAIRS"
pfh10RepairsEndPartBE = r"03-CER-PREE\02-CER indB - BE"
#testPath = r"C:\Users\jt30320l\Box Sync\y_POLE REGULATION\01 - Suivi PFH\8 - Partage CER\Test"
#tryPath = r"C:\Users\503404681\Box\y_POLE REGULATION\01 - Suivi PFH\8 - Partage CER\CER\ATTENTE VALIDATION CLIENT\Essai"

def thereIsOnlyDirs(subPath): # Check if there is only directories in this folder
    obj = os.scandir(subPath) #Scan the dir and get iterable object
    so = True
    for entry in obj:
        if entry.is_file() or entry.is_symlink(): #Break the loop at the first occurence of a symlink or file
            so = False
            break

    return so

def getCERName(parentPath):
    obj = os.scandir(parentPath)

    rawName = ""
    for entry in obj:
        if entry.name.startswith("CER_B") or entry.name.startswith("CER"): #Find the file with the name starting with either options 
            rawName = entry.name.split() #Split to isolate the last block for further use
            break
    
    return rawName

def removeExtension(rawName):
    try:
        buffer = rawName[-1].split(".") #Seperate the last part of the name and the extension name
    except IndexError: #This is certainly due to an emtpy string
        msg = "Il n'y a pas de fichier commençant par 'CER' ou 'CER_B'. Une chaîne vide continue le process.\n"
        writeToInternalLog(msg)
        return rawName

    del rawName[-1] #Delete the whole block
    rawName.append(buffer[0]) #Get back last part without the extension name in the main list
    return rawName


def createTargetDirectoryName(buffer): 

    finalLine = ""
    #Getting id number
    try: #In this case the filename begin with CER followed by a space i.e CER 24-10
        nums = buffer[1].split("-")
        num = int (nums[1])
        i = 2 #This is the index of the first part of the machine's name its value change according to name's beginning
    except IndexError: #In this one, the file's name begin with CER followed by the id number with no space i.e CER24-10
        try:
            nums = buffer[0].split("-") 
            num = int (nums[1])
            i = 1 #This is the index of the first part of the machine's name its value change according to name's beginning
        except IndexError:
            msg = "Le format du nom du fichier CER ne permet pas la création du dossier.\n"
            writeToInternalLog(msg)
            return ""

    if num < 10 : #Adding a 0 at the beginnig to keep the naming style
        num = "0" + str(num)
    else:
        num = str(num)

    #Getting OTP
    otp = buffer[-1]

    #Getting machine's name
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
        #Final Line Merging
        finalLine = num + " " + otp + " " + name

    return finalLine

def createTargetDirectory (sourcePath, targetPath):

    dirName = getCERName(sourcePath)
    dirName = removeExtension(dirName)
    if dirName == "":
        msg = f'La chaîne de caractères reçue ne permet pas de créer le dossier CER lié à : "{sourcePath}".\n'
        writeToInternalLog(msg)
        return ""
    dirName = createTargetDirectoryName(dirName)
    if dirName == "":
        msg = f'La chaîne de caractères reçue ne permet pas de créer le dossier CER lié à : "{sourcePath}".\n'
        writeToInternalLog(msg)
        return ""
    finalPath = os.path.join(targetPath,dirName)

    try:
        os.makedirs(finalPath, exist_ok=True)
    except OSError:
        print ("Le dossier " + finalPath + " ne peut être crée")

    return finalPath

#def writeDirNameToFile ():

def copyFilesToPoleReg(sourcePath, targetPath):
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


def getOTPandPT(buffer):
    #Getting OTP
    otp = buffer[-1]
    if not (otp.startswith("IS0") or otp.startswith("ES0")):
        otp = ""
        msg = f'L\'OTP n\'est pas au bon format.\n'
        writeToInternalLog(msg)

    #Getting PT
    pt = ""
    try:
        index = 1
        while index : #delete all "-"
            index = buffer.index("-")
            del buffer[index]
    except ValueError: #It means that there is no "-" used in the filename except in the OTP
        pt = buffer[-2]
        if not pt.startswith("PT"):
            pt = ""
            msg = f'Le n° de PT n\'est pas au bon format.\n'
            writeToInternalLog(msg)

    return otp, pt

def findTargetDirectory(buffer, targetPath, endPart):
    otp, pt = getOTPandPT(buffer)
    if otp == "" or pt == "":
        msg = f'La sélection du dossier cible n\'est pas possible.\n'
        writeToInternalLog(msg)
        return ""

    obj = os.scandir(targetPath)
    for entry in obj:
        temp = entry.name.split()
        temp = temp[0]
        if temp.startswith("ES0") or temp.startswith("IS0"): #Check if the current directory starts with the right OTP format
            if temp == otp :
                newTargetPath = os.path.join(targetPath, entry.name)
                obj2 = os.scandir(newTargetPath)
                for entry2 in obj2:
                    temp2 = entry2.name.split()
                    temp2 = temp2[-1]
                    if temp2.startswith("PT"): #Check if the current directory starts with the right PT format
                        if temp2 == pt:
                            target = os.path.join(newTargetPath, entry2.name)
                            target = os.path.join(target,endPart)
                            return target
                    else:
                        newTargetPath = os.path.join(targetPath, entry2.name)
                        msg = f'Le n° PT est absent ou son format est mauvais dans : "{newTargetPath}".\n'
                        writeToInternalLog(msg)
        else:
            newTargetPath = os.path.join(targetPath, entry.name)
            msg = f'L\'OTP est absent ou son format est mauvais dans : "{newTargetPath}".\n'
            writeToInternalLog(msg)
    return ""

def selectTargetDirectory(sourcePath, targetPath, endPart):
    dirName = getCERName(sourcePath)
    dirName = removeExtension(dirName)
    if dirName == "":
        msg = f'La chaîne de caractères reçue ne permet pas de trouver le dossier CER lié à : "{sourcePath}".\n'
        writeToInternalLog(msg)
        return ""
    target = findTargetDirectory(dirName, targetPath, endPart)
    if target == "":
        msg = f'La copie n\'est pas possible vers : "{targetPath}".\n'
        writeToInternalLog(msg)
    return target


def copyFilesToPFH10(sourcePath, targetPath, endPart):
    obj = os.scandir(sourcePath)
    if thereIsOnlyDirs(sourcePath):
        for entry in obj: #Iterate until you get inside the machine's directory containing both files and directories
            print("Only Dirs")
            print(entry.name)
            newSourcePath = os.path.join(sourcePath, entry.name)
            copyFilesToPFH10(newSourcePath, targetPath, endPart)
    else:
        target = selectTargetDirectory(sourcePath, targetPath, endPart)
        if target == "":
            pass
        else:
            command = f'robocopy "{sourcePath}" "{target}" CER* /COPY:DATSO /UNILOG+:output.txt /ETA /TEE'  #See help robocopy in a cmd to get more details
            os.system(command)


#a = r"C:\Users\503404681\Box\y_POLE REGULATION\01 - Suivi PFH\8 - Partage CER\CER\Test"
#b = r"03-CER-PREE\02-CER indB - BE"

#command = f'robocopy "{a}" "{b}" CER* /COPY:DATSO /UNILOG+:output.txt /ETA /TEE'  #See help robocopy in a cmd to get more details
#os.system(command)

copyFilesToPoleReg(homePath, poleRegCERPath)
copyFilesToPFH10(homePath, pfh10RepairsPath, pfh10RepairsEndPartBE)