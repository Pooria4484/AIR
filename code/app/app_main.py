from .ui import *
from .config import*
from .setting import*
import uasyncio
import asocket
from save import *
from wifi import *


from wifi import ap
ap(s='AIR',p='msb-co.ir')
try:
    from . version import version as app_ver
except ImportError:
    print('no release it is debug')
dh=dht()#dht set pin and type default pin 32 - type dht22 
if dh==None:
    set_dht(type='11')
    dh=dht()
server=asocket.Server()#socket server object
loop=uasyncio.get_event_loop()
tempTimer = Timer(0)
from gc import collect,mem_free
#wdt = WDT(timeout=15000)  # enable wdt it with a timeout of 15s
wdt=None
ui=UI(oled,wdt)
print('MEM Free',mem_free())
collect()
print('MEM Free',mem_free())

buzzCnt=1
data=''
rx_flag=False#socket inbox handle flag
tTimerFlag=False#temp timer handle flag
def TempTimer(tempTimer):
    global tTimerFlag
    tTimerFlag=True
def SocketRx(Data):
    global rx_flag,data
    data=Data
    rx_flag=True
async def main():
    global tTimerFlag,mTimerFlag,fTimerFlag,rx_flag,data,buzzCnt
    tahandle=gettahe()#temp and hum auto handle with timer in case off sensor err
    err=0
    therr=False#temp and hum error flag
    cnt=0#main loop counter
    tcnt=0#main loop 10 ms counter
    therrcnt=0#th error counter
    tec=10#current temp var
    huc=10#current hum var
    #hug=gethug()#goal hum
    teg=getteg()#goal temp
    tse=gettse()#temp system enable
    #hse=gethse()#hum system enable
    gse=getgse()#gas system enable
    #fte=getfte()#fan timer enable
    tte=gettte()#temp timer enable
    #mte=getmte()#mist timer enable
    #fton=getfton()#fan timer on time
    #ftoff=getftoff()#fan timer off time
    #mton=getmton()#mist timer on time
    #mtoff=getmtoff()#mist timer off time
    tton=gettton()#temp timer on time
    ttoff=getttoff()#temp timer off time
    ttfast=getttfast()#temp timer fast time
    #etse=getetse()#external temp sensor enabl
    #ftrefresh=False #timers value changed
    ttrefresh=False
    #mtrefresh=False
    thErrHandled=False
    errBuzzCnt=0 
    print(rtc.datetime()[4:7])

    if tte:
        tempTimer.init(period=5000, mode=Timer.ONE_SHOT, callback=TempTimer)

    # up_cnt=0#up touch counter in 10ms
    # down_cnt=0#down touch counter in 10ms
    # ok_cnt=0#ok touch counter in 10ms
    # page=0#ui page number
    # item=0#ui item number
    # mistOn=False
    mcnt=0
    while True:
        if tcnt%13==0:
            if ttrefresh:
                ttrefresh=False
                tempTimer.deinit()
                if tte or (tahandle and therr):
                    cooler_motor.off()
                    cooler_water.off()
                    cooler_speed.off()
                    tempTimer.init(period=200, mode=Timer.ONE_SHOT, callback=TempTimer)
            cnt+=1      

            if cnt%7==0:
                server.send('*#wake@$\r\n')
                
            if dh!=None:
                    try:
                        dh.measure()    
                        huc=dh.humidity()
                        tec=dh.temperature()
                        therr=False                    
                        if err==1:
                            err=0#resolve error
                            ui.set_err(0)
                        therrcnt=0

                    except Exception as e:
                        therrcnt+=1
                        if therrcnt>30:#wait for 30 cnt
                            therr=True                    
                            therrcnt=0    
                            if err==0:
                                ui.set_err(1)#show error
                                err=1
            if not therr and therrcnt==0:#if temp and hum sensor has no error and errcnt is zero show tec and huc
                    ui.set_temp_hum(tec,huc)
            
            if therr:
                if errBuzzCnt>10:
                    errBuzzCnt=0
                    buzzCnt=3   
                errBuzzCnt+=1
                if not thErrHandled:
                    if tahandle:
                        thErrHandled=True
                        if (not mte) and hse:
                            mtrefresh=True
                            print('handle-hse')         
                        if (not tte) and tse:
                            ttrefresh=True  
                            print('handle-tse')         
            else:
                if thErrHandled:
                    if not tte:
                        ttrefresh=True
                    thErrHandled=False    


            #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
            if rx_flag:#handle messages from socket client
                rx_flag=False
                a = data.find('*#')
                b = data.find('@$')
                cmnd=''
                if a!=-1 and b>a:#check for start and end
                    cmnd=data[a+2:b]
                    #sssssssssssssssssssssssssssssssssssssssssssync
                    if cmnd.find('sync')!=-1:#check for sync command
                        buff='*#huc'+str(int(huc*10))+'hug'+str(hug)
                        if tec>9:
                            buff+='tec'+str(int(tec*10))+'teg'+str(teg)
                        else:
                            buff+='tec0'+str(int(tec*10))+'teg'+str(teg)    

                        if tton>9:    
                            buff+='tton'+str(tton)
                        else:
                            buff+='tton0'+str(tton)

                        if ttoff>9:
                            buff+='ttoff'+str(ttoff)
                        else:
                            buff+='ttoff0'+str(ttoff)

                        if ttfast>9:
                            buff+='ttfast'+str(ttfast)
                        else:
                            buff+='ttfast0'+str(ttfast)    
                        
                        #buff2='RLH'+str(heater_valve.value())+str(heater_fan.value())+'M'+str(mist.value())+'F'+str(fan.value())+'C'+str(cooler_water.value())+str(cooler_motor.value())+str(cooler_speed.value())
                        #buff+=buff2
                        
                        if tse:
                            buff+='-TSE-'
                        else:
                            buff+='-TSD-'

                        if tte:
                            buff+='-TTE-'
                        else:
                            buff+='-TTD-'

                        if gse:
                            buff+='-GSE-'
                        else:
                            buff+='-GSD-'
                            
                        if tahandle:
                            buff+='-TAHE-'
                        else:
                            buff+='-TAHD-'
                        

                        buff2="NOW"+str(rtc.datetime()[4:7]) 

                        buff+=buff2
                        buff2="ver"+app_ver
                        buff+=buff2+"@$\r\n"
                        server.send(buff)   
                        buzzCnt=1 
                    else:
                        print(cmnd)
                        buzzCnt=2

                    #system enabled and disable command
                    if cmnd.find('TSE')!=-1:#temp system
                        tse=settse(True)
                    if cmnd.find('TSD')!=-1:
                        tse=settse(False)   

                    if cmnd.find('GSE')!=-1:#gas system
                        gse=setgse(True)
                    if cmnd.find('GSD')!=-1:
                        gse=setgse(False)  

                        

                    if cmnd.find('TTE')!=-1:#temp timer
                        tte=settte(True)
                        ttrefresh=True

                    if cmnd.find('TTD')!=-1:
                        tte=settte(False)
                        ttrefresh=True



                    if cmnd.find('UPDATE')!=-1:#app update enabled (OTA)
                        save('update','True')
                        print('update','True')


                    #change ap config
                    a = cmnd.find('APSSID')
                    b = cmnd.find('PASS')
                    c = cmnd.find('END')
                    if a!=-1 and b>a and c>b:
                        ssid=cmnd[a+6:b]
                        password=cmnd[b+4:c]
                        ap(s=ssid,p=password)
                        print('AP==>',ssid,password)


                    #change sta config
                    a = cmnd.find('STASSID')
                    b = cmnd.find('PASS')
                    c = cmnd.find('END')
                    if a!=-1 and b>a and c>b:
                        ssid=cmnd[a+7:b]
                        password=cmnd[b+4:c]
                        sta(s=ssid,p=password)
                        print('STA==>',ssid,password)

                    #goal temp
                    a = cmnd.find('teg')
                    if a!=-1:
                        teg=setteg(a,cmnd)


                    #timers values change


                    a = cmnd.find('tton')
                    if a!=-1:
                        tton=settton(a,cmnd)
                        ttrefresh=True
                        

                    a = cmnd.find('ttoff')
                    if a!=-1:
                        ttoff=setttoff(a,cmnd)                        
                        ttrefresh=True


                    a = cmnd.find('ttfast')
                    if a!=-1:
                        ttfast=setttfast(a,cmnd)
                        ttrefresh=True
                        


                    a = cmnd.find('TAHE')
                    if a!=-1:
                        tahandle=settahe(True)

                    a = cmnd.find('TAHD')
                    if a!=-1:
                        tahandle=settahe(False)    
                        

                    a = cmnd.find('ver')
                    if a!=-1:    
                        buff='app ver==>'+app_ver+'\r\n'
                        server.send(buff)                


            if tcnt%100==0:
                if tse and (not tte):#if temp system enabled and temp timer disabled
                    if not therr:#if temp has no err
                        if tec>(teg+3.0):#vary very hot
                            
                            if(cooler_water.value()!=1):
                                cooler_water.on()
                                # await uasyncio.sleep_ms(250)
                                cooler_motor.on()
                            if(cooler_speed.value()!=1):                    
                                # await uasyncio.sleep_ms(250)
                                cooler_speed.on()


                        elif tec>(teg+1.5):#ver hot

                                            
                            if(cooler_motor.value()!=1):
                                cooler_water.on()
                                # await uasyncio.sleep_ms(250)
                                cooler_motor.on()
                                # await uasyncio.sleep_ms(250)
                            if(cooler_speed.value()==1):                        
                                cooler_speed.off()

                            if(cooler_motor.value()==1):
                                cooler_water.off()
                                # await uasyncio.sleep_ms(250)
                                cooler_motor.off()
                                # await uasyncio.sleep_ms(250)
                            if(cooler_speed.value()==1):                        
                                cooler_speed.off()


                        elif tec<(teg-1.0):#cold
                            if(cooler_motor.value()==1):
                                cooler_water.off()
                                # await uasyncio.sleep_ms(250)
                                cooler_motor.off()
                                # await uasyncio.sleep_ms(250)
                            if(cooler_speed.value()==1):                        
                                cooler_speed.off()            
                    else:#temp err
                        if (not tahandle):#temp error auto handle
                            cooler_motor.off()
                            cooler_speed.off()
                            cooler_water.off()
                else:#temp system off
                    if not tte:
                        cooler_motor.off()
                        cooler_speed.off()
                        cooler_water.off()


                if gse:#gas system enabled
                    pass

            if(tTimerFlag):
                tTimerFlag=False
                if tte or (tahandle and therr):
                    if cooler_water.value()==0:
                        cooler_water(1)
                        cooler_motor(1)
                        if ttfast!=0:
                            cooler_speed(1)
                            tt=ttfast
                        else:
                            cooler_speed(0)    
                            tt=tton
                    else:
                        if ttfast!=0:
                            if cooler_speed.value()==1:
                                tt=tton
                            else:
                                tt=ttoff        
                                cooler_motor(0)
                                cooler_water(0)
                        else:
                            tt=ttoff
                            cooler_motor(0)
                            cooler_water(0)                            
                        cooler_speed(0)        
                    tempTimer.init(period=tt*60000, mode=Timer.ONE_SHOT, callback=TempTimer)
                    print('tTimer reached','water',cooler_water.value(),'motor',cooler_motor.value(),'speed',cooler_speed.value(),rtc.datetime()[4:7])


        tcnt+=1
        mcnt+=1
        await uasyncio.sleep_ms(25)


async def BuzzTask():
    global buzzCnt
    while True:
        if buzzCnt>0:
            if buzz.value()==0:
                buzz.on()
            else:
                buzzCnt-=1
                buzz.off()
        await uasyncio.sleep_ms(75)


server.set_rlistener(SocketRx)
loop.create_task(server.run(loop))
loop.create_task(ui.Run())
loop.create_task(BuzzTask())
try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    print('Interrupted')
finally:
  server.close()        
