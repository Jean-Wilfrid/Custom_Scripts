"""
Author : Jean-Wilfrid TOGNIBO
First release date : 18/03/2025 (date format : DD/MM/YYYY)
The aim of this code is to setup the working folder at the begining of a PREE 
"""

import os

#The copy of the FA is missing should be added and automated
dest = r"C:\Temp_Perso"
sourcePFH01 = r"C:\Users\jt30320l\Box\Plateforme Hydraulique - GAIA\PFH01-Remise en état\2025\IS0-800555 - CHOOZ - CIVAUX\AEH SMR\PT25118_B - AEH SMR"
sourcePFH10 = r"C:\Users\jt30320l\Box\Plateforme Hydraulique - GAIA\PFH10-SDP interservices\REPAIRS\IS0-800555 - CHOOZ et CIVAUX - 6 AEH\AEH SMR - PT25118\03-CER-PREE\01-CER indA - Atelier"
source = r"C:\Temp_Perso\PREE\IS0-800555\Essai"
""" 
In the use of robocopy, attributes S,O and U of the parameter /COPY are not useful. Copied files inherit of the corresponding values of these attributes from the destination folder. Then there is no need to copy them in our usecase.
See help robocopy in the command line and the following links for more details.
https://forum.clubic.com/t/utilisation-de-robocopy-pour-sauvegarde-sur-un-nas/399697/3
https://www.malekal.com/autorisations-permissions-fichiers-ntfs-partage-dossier-windows/
"""

def copyFromPFH01(source, dest): #Copy all dats except the pdf and excel files. They will be copied by another function.
    command = f'robocopy "{source}" "{dest}" /E /COPY:DT /DCOPY:DTE /UNILOG+:initOutput.txt /MT[:16] /ETA /TEE /XF *.pdf *.xlsx'
    os.system(command)

def copyFromPFH10(source, dest): #Copy all files from source to destination. The files in this folder are supposed to be the last version validated.
    command = f'robocopy "{source}" "{dest}" /E /COPY:DT /DCOPY:DTE /UNILOG+:initOutput.txt /MT[:16] /ETA /TEE'
    os.system(command)

copyFromPFH01(sourcePFH01, dest)
copyFromPFH10(sourcePFH10, dest)
