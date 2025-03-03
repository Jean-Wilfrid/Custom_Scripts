import os

a = r"C:\Users\503404681\Box\y_POLE REGULATION\01 - Suivi PFH\8 - Partage CER\CER\Essai"
b = r"C:\Users\503404681\Box\y_POLE REGULATION\01 - Suivi PFH\8 - Partage CER\CER\Try"

command = f'robocopy "{a}" "{b}" CER* /COPY:DATSO /UNILOG+:output.txt /ETA /TEE'  #See help robocopy in a cmd to get more details
os.system(command)