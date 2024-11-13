
def getKey():
    f=open("./Resources/Credential/GPTApi.txt",'r')
    api=f.readline()
    f.close()
    return api
