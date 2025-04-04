def rightOTPFormat(otp :str)-> bool:#Check if the string received agrees with OTP FORMAT
    """
    Here is the format definition. The OTP is a string of two blocks seperated by a dash (-).
    The first block is a combination of two letter and a zero (0). Currently, this block is 
    "IS0" or "ES0". The second block is series of six digits. Currently, the first digit is 
    always 8. Some examples : IS0-800574, ES0-801555.
    """
    temp = otp.split("-")
    if len(temp) != 2:#Check if it is two blocks seprated by a dash (-) 
        return False
    else:
        if not (temp[0].startswith("IS0") or temp[0].startswith("ES0")):#Check if it startswith "IS0" or "ES0"
            return False
        else:#Check if it ends with a series of digits.
            try:
                temp2 = int(temp[1])
                return True
            except ValueError:
                return False

def rightPTFormat(pt : str) -> bool:#Check if the string received agrees with PT FORMAT
    """
    Here is the format definition. PT is a id number made of characters 'P' and 'T'
    followed by a series of number. There is no space between them. Some examples : PT1193, PT15850.
    """
    temp = pt.split()
    if len(temp) > 1 :#If is seperated by space
        return False
    else:
        if not pt.startswith("PT"):
            return False
        else:
            temp2 =""
            i = 2
            while i <= len(pt) - 1 :#There is a shorter way to code this. But I discovered it once this was coded. As we say in french :"Flemme"
                temp2 = temp2.__add__(pt[i])
                i += 1
            try:#If the remaining part is series of number
                temp2 = int(temp2)
                return True
            except ValueError:
                return False
