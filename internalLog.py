def writeToInternalLog(msg):
    print(msg)
    file = open("internal_log.txt", "a+", encoding="utf-8")
    file.write(msg)
    file.close()