#The aim of this code is to setup the working folder at the begining of a PREE 
import os

dest = r"C:\Temp_Perso\PREE\IS0-800555\AEH SMR PT15736_E"
sourcePFH01 = r"C:\Users\jt30320l\Box\Plateforme Hydraulique - GAIA\PFH01-Remise en état\2025\IS0-800555 - CHOOZ - CIVAUX\AEH SMR\PT15736_E - AEH SMR"
sourcePFH10 = r"C:\Users\jt30320l\Box\Plateforme Hydraulique - GAIA\PFH10-SDP interservices\REPAIRS\IS0-800555 - CHOOZ et CIVAUX - 6 AEH\AEH SMR MP - PT15736\03-CER-PREE\01-CER indA - Atelier"


def copyFromPFH01(source, dest): #Copy all dats except the pdf and excel files. They will be copied by another function.
    command = f'robocopy "{source}" "{dest}" /E /COPY:DATSO /DCOPY:DATE /UNILOG+:initOutput.txt /MT[:16] /ETA /TEE /XF .pdf .xlsx'
    os.system(command)

def copyFromPFH10(source, dest): #Copy all files from source to destination. The files in this folder are supposed to be the last version validated.
    command = f'robocopy "{source}" "{dest}" /E /COPY:DATSO /DCOPY:DATE /UNILOG+:initOutput.txt /MT[:16] /ETA /TEE'
    os.system(command)

copyFromPFH01(sourcePFH01, dest)
copyFromPFH10(sourcePFH10, dest)