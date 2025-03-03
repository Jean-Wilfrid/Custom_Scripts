import os 

otpList =["IS0-800389","IS0-800393","IS0-800395","IS0-800396","IS0-800438","IS0-800440","IS0-800441","IS0-800442","IS0-800443"]

path = r"C:\Users\503404681\Box\Plateforme Hydraulique - GAIA\PFH10-SDP interservices\REPAIRS"
dest = r"C:\Users\503404681\Box\y_POLE REGULATION\01 - Suivi PFH\8 - Partage CER\CER\Test"

def copyFiles (path, dest, otpList):
    obj = os.scandir(path)
    for entry in obj:
        buffer = entry.name.split()
        buffer = buffer[0]
        if not buffer.startswith("IS0"):
            continue
        else:
            for elt in otpList:
                if buffer == elt :
                    sourcePath = os.path.join(path, entry.name)
                    finalDest = os.path.join(dest,entry.name)
                    command = f'robocopy "{sourcePath}" "{finalDest}" /E /COPY:DATSO /DCOPY:DATE /UNILOG+:copyOutput.txt /MT[:16] /ETA /TEE'
                    os.system(command)


copyFiles(path, dest, otpList)
