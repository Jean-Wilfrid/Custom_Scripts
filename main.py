import diffusionRevB as drb

homePath = r"C:\Users\jt30320l\Box\y_POLE REGULATION\01 - Suivi PFH\8 - Partage CER\CER\Attente validation client\IS0-800574 Relais MEM"
poleRegCERPath = r"C:\Users\jt30320l\Box\y_POLE REGULATION\01 - Suivi PFH\2 - Expertise\Z_EXPERTISE 2025" #Try to automate the choice of this folder later
pfh10RepairsPath = r"C:\Users\jt30320l\Box\Plateforme Hydraulique - GAIA\PFH10-SDP interservices\REPAIRS"
pfh10RepairsEndPartBE = r"03-CER-PREE\02-CER indB - BE"

drb.copyFilesToPoleReg(homePath, poleRegCERPath)
drb.copyFilesToPFH10(homePath, pfh10RepairsPath, pfh10RepairsEndPartBE)