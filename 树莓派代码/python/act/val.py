from time import sleep
vol=0.5
def voldown():
    for i in range(5):
        global vol
        vol=0.5-i/10
        sleep(0.05)
def getvol():
    global vol
    return vol
def volup():
    for i in range(5):
        global vol
        vol=i/10+0.1
        sleep(0.05)
if __name__=="__main__":
    voldown()
    print(getvol())
    sleep(1)
    volup()
    print(getvol())