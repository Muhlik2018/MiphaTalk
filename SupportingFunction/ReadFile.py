
def getCharacter():
    f=open("./Resources/GPT/Character.txt",'r')
    api=f.readline()
    f.close()
    return api

def getKey():
    f=open("./Resources/GPT/GPTApi.txt",'r')
    api=f.readline()
    f.close()
    return api
