file1 = open("source.txt","r") #open source file in read mode

sourceText = file1.readlines() #read all the file's lines in a list
finalLine = ""
finalText = []

for sourceLine in sourceText : #extracting data from read file
    buffer = sourceLine.split()

    #Getting id number
    nums = buffer[1].split("-")
    num = int (nums[1])
    num = str(num)

    #Getting OTP
    otp = buffer[-1]

    #Getting machine's name
    name = ""
    index = buffer.index("-")
    i = 2 #This is always the index of the first part of the machine's name
    while i < index - 1 : #Merging all the parts in a single name
        name += buffer[i]
        name += " "
        i += 1
    name += buffer[index - 1]

    #Final Line Merging
    finalLine = num + " " + otp + " " + name + " " + buffer[index + 1] + "\n"
    finalText.append(finalLine)

    print(finalText)

file1.close()

file2 = open("output.txt","w+")

file2.writelines(finalText)

file2.close()