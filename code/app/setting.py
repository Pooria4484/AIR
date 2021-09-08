from save import *
from dht import DHT22,DHT11
from machine import Pin

def set_dht(p=32,type='22'):#set dht sensor pin and type
    save('dht',type)
    save('dht_pin',str(p))

def dht():
    try:
        buff=load('dht')
        val=load('dht_pin')
        if int(buff)==22:
            d=DHT22(Pin(int(val)))
        else :
            d=DHT11(Pin(int(val)))           
    except KeyError:
        d=None
    return d    



def getteg():
    try:
        try:
            return int(load("teg").decode('utf-8'))
        except ValueError:
            save('teg','25')    
            return 25
    except KeyError:
        save('teg','25')    
        return 25

def gethug():
    try:
        try:
            return int(load('hug').decode('utf-8'))
        except ValueError:
            save('hug','50')
            return  50
    except KeyError:
        save('hug','50')
        return  50

def setteg(a,cmnd):
    try:
        val=int(cmnd[a+3:a+5])
        print('teg==>',val)
        save('teg',str(val))
        return val
    except ValueError:
        print('teg==>','wrong value')
        return getteg()
def sethug(a,cmnd):
    try:
        val=int(cmnd[a+3:a+5])
        print('hug==>',val)
        save('hug',str(val))
        return val
    except ValueError:
        print('hug==>','wrong value')
        return gethug()

def gettse():
    try:
        try:
            if load('tse').decode('utf-8')=='False':
                return False
            else:
                return True
        except ValueError:
            save('tse',str(True))
            return  True
    except KeyError:
        save('tse',str(True))
        return  True


def settse(b):
    try:        
        print('tse==>',b)
        save('tse',str(b))
        return b
    except ValueError:
        print('tse==>','wrong value')
        return gettse()


def getetse():
    try:
        try:
            if load('etse').decode('utf-8')=='False':
                return False
            else:
                return True
        except ValueError:
            save('etse',str(True))
            return  True
    except KeyError:
        save('etse',str(True))
        return  True


def setetse(b):
    try:        
        print('etse==>',b)
        save('etse',str(b))
        return b
    except ValueError:
        print('etse==>','wrong value')
        return getetse()



def gethse():
    try:
        try:
            if load('hse').decode('utf-8')=='True':
                return True
            else:
                return False
        except ValueError:
            save('hse',str(False))
            return  False
    except KeyError:
        save('hse',str(False))
        return  False


def sethse(b):
    try:        
        print('hse==>',b)
        save('hse',str(b))
        return b
    except ValueError:
        print('hse==>','wrong value')
        return gethse()



def getgse():
    try:
        try:
            if load('gse').decode('utf-8')=='True':
                return True
            else:
                return False
        except ValueError:
            save('gse',str(False))
            return  False
    except KeyError:
        save('gse',str(False))
        return  False


def setgse(b):
    try:        
        print('gse==>',b)
        save('gse',str(b))
        return b
    except ValueError:
        print('gse==>','wrong value')
        return getgse()



def getfte():
    try:
        try:
            if load('fte').decode('utf-8')=='True':
                return True
            else:
                return False
        except ValueError:
            save('fte',str(False))
            return  False
    except KeyError:
        save('fte','False')
        return  False


def setfte(b):
    try:        
        print('fte==>',b)
        save('fte',str(b))
        return b
    except ValueError:
        print('fte==>','wrong value')
        return getfte()


def gettte():
    try:
        try:
            if load('tte').decode('utf-8')=='True':
                return True
            else:
                return False
        except ValueError:
            save('tte',str(False))
            return  False
    except KeyError:
        save('tte',str(False))
        return  False


def settte(b):
    try:        
        print('tte==>',b)
        save('tte',str(b))
        return b
    except ValueError:
        print('tte==>','wrong value')
        return gettte()


def setftoff(a,cmnd):
    try:
        print(cmnd[a+5:a+7])
        val=int(cmnd[a+5:a+7])
        print('ftoff==>',val)
        save('ftoff',str(val))
        return val
    except ValueError:
        print('ftoff==>','wrong value')
        return getftoff()

def setfton(a,cmnd):
    try:
        print(cmnd[a+4:a+6])
        val=int(cmnd[a+4:a+6])
        print('fton==>',val)
        save('fton',str(val))
        return val
    except ValueError:
        print('fton==>','wrong value')
        return getfton()



def getfton():
    try:
        try:
            return int(load('fton').decode('utf-8'))
        except ValueError:
            save('fton','10')
            return  10
    except KeyError:
        save('fton','10')
        return  10


def getftoff():
    try:
        try:
            return int(load('ftoff').decode('utf-8'))
        except ValueError:
            save('ftoff','50')
            return  50
    except KeyError:
        save('ftoff','50')
        return  50


def getmte():
    try:
        try:
            if load('mte').decode('utf-8')=='True':
                return True
            else:
                return False
        except ValueError:
            save('mte',str(False))
            return  False
    except KeyError:
        save('mte',str(False))
        return  False


def setmte(b):
    try:        
        print('mte==>',b)
        save('mte',str(b))
        return b
    except ValueError:
        print('mte==>','wrong value')
        return gettte()




def setmtoff(a,cmnd):
    try:
        val=int(cmnd[a+5:a+7])
        print('mtoff==>',val)
        save('mtoff',str(val))
        return val
    except ValueError:
        print('mtoff==>','wrong value')
        return getmtoff()
def setmton(a,cmnd):
    try:
        val=int(cmnd[a+4:a+6])
        print('mton==>',val)
        save('mton',str(val))
        return val
    except ValueError:
        print('mton==>','wrong value')
        return getmton()



def getmton():
    try:
        try:
            return int(load('mton').decode('utf-8'))
        except ValueError:
            save('mton','10')
            return  10
    except KeyError:
        save('mton','10')
        return  10


def getmtoff():
    try:
        try:
            return int(load('mtoff').decode('utf-8'))
        except ValueError:
            save('mtoff','50')
            return  50
    except KeyError:
        save('mtoff','50')
        return  50




def setttoff(a,cmnd):
    try:
        val=int(cmnd[a+5:a+7])
        print('ttoff==>',val)
        save('ttoff',str(val))
        return val
    except ValueError:
        print('ttoff==>','wrong value')
        return getttoff()
def settton(a,cmnd):
    try:
        val=int(cmnd[a+4:a+6])
        print('tton==>',val)
        save('tton',str(val))
        return val
    except ValueError:
        print('tton==>','wrong value')
        return gettton()



def gettton():
    try:
        try:
            return int(load('tton').decode('utf-8'))
        except ValueError:
            save('tton','10')
            return  10
    except KeyError:
        save('tton','10')
        return  10


def getttoff():
    try:
        try:
            return int(load('ttoff').decode('utf-8'))
        except ValueError:
            save('ttoff','50')
            return  50
    except KeyError:
        save('ttoff','50')
        return  50




def setttfast(a,cmnd):
    try:
        val=int(cmnd[a+6:a+8])
        print('ttfast==>',val)
        save('ttfast',str(val))
        return val
    except ValueError:
        print('ttfast==>','wrong value')
        return getttfast()



def getttfast():
    try:
        try:
            return int(load('ttfast').decode('utf-8'))
        except ValueError:
            save('ttfast','2')
            return  2
    except KeyError:
        save('ttfast','2')
        return  2


def gettahe():
    try:
        try:
            if load('tahe').decode('utf-8')=='True':
                return True
            else:
                return False
        except ValueError:
            save('tahe',str(False))
            return  False
    except KeyError:
        save('tahe','False')
        return  False

def settahe(b):
    try:        
        print('tahe==>',b)
        save('tahe',str(b))
        return b
    except ValueError:
        print('tahe==>','wrong value')
        return gettahe()

