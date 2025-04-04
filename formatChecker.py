def rightOTPFormat(otp :str)-> bool:#Check if the string received agrees wih OTP FORMAT
    """Here is the format definition. The OTP is a string of two blocks seperated by a dash (-).
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

