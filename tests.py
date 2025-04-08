"""
https://realpython.com/python-testing/#automated-vs-manual-testing

"""

import diffusionRevB as drb

homePath = r"C:\Home\PREE\Test\Attente"
poleRegCERPath = r"C:\Home\PREE\Test\Pole_Reg"
pfh10RepairsPath = r"C:\Users\jt30320l\Box\Plateforme Hydraulique - GAIA\PFH10-SDP interservices\REPAIRS"
pfh10RepairsEndPartBE = r"03-CER-PREE\02-CER indB - BE"

drb.copyFilesToPoleReg(homePath, poleRegCERPath)
#drb.copyFilesToPFH10(homePath, pfh10RepairsPath, pfh10RepairsEndPartBE)