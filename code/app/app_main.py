from .config import*
import uasyncio
import asocket
from save import *
from wifi import *
from .ui import *
ap(s='AIR',p='msb-co.ir')
loop=uasyncio.get_event_loop()
from gc import collect,mem_free
from dht import DHT11
dh=DHT11(Pin(32))
dh.measure()
#wdt = WDT(timeout=15000)  # enable wdt it with a timeout of 15s
wdt=None
ui=UI(oled,wdt)
print('MEM Free',mem_free())
collect()
print('MEM Free',mem_free())
buzzCnt=1

async def main():
    global buzzCnt
    wcnt=0
    ucnt=0
    dcnt=0
    ocnt=0
    u=up()
    d=down()
    o=ok()
    uf=False
    df=False
    of=False
    tec=0
    teg=25
    huc=0
    while True:
        if wcnt>25:
            print(rtc.datetime()[4],':',rtc.datetime()[5],':',rtc.datetime()[6],'-->',
            'W',cooler_water(),'M',cooler_motor(),'S',cooler_speed(),'--- T:',tec,'H:',huc)
            wcnt=0
            try:
                dh.measure()
                huc=dh.humidity()
                tec=dh.temperature()
                ui.set_temp_hum(tec,huc)
            except Exception as e:
                pass    
                print('err-->',e)



        
        if up()!=u:
            u=up()
            if ucnt==0:
                uf=True
                ucnt=6
        if down()!=d:
            d=down()
            if dcnt==0:
                df=True
                dcnt=6
        if ok()!=o:
            o=ok()
            if ocnt==0:
                of=True
                ocnt=6
        if of and df:
            buzzCnt=2
            print('do')
        elif uf and of:
            buzzCnt=2
            print('uo')
        elif uf:
            buzzCnt=1
            cooler_water(not cooler_water())
            print('u')
        elif df:
            buzzCnt=1      
            cooler_speed(not cooler_speed())          
            print('d')
        elif of:
            buzzCnt=1    
            cooler_motor(not cooler_motor())
            print('o')
        of=False
        df=False    
        uf=False
        if ocnt!=0:
            ocnt-=1
        if ucnt!=0:
            ucnt-=1    
        if dcnt!=0:
            dcnt-=1    



        await uasyncio.sleep_ms(40)
        wcnt+=1


async def BuzzTask():
    global buzzCnt
    while True:
        if buzzCnt>0:
            if buzz()==0:
                buzz(1)
            else:
                buzzCnt-=1
                buzz(0)
        await uasyncio.sleep_ms(100)
loop.create_task(ui.Run())
loop.create_task(BuzzTask())
try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    print('Interrupted')
finally:
  pass
  # server.close()        
