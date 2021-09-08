import uasyncio
import framebuf
class UI:    
    def _show_num_32(self,n,x,y):
        self.oled.fill_rect(x,y,43,32,0)   
        d=int(n/10)%10
        path='bin/dig32/'+str(d)
        if d==1:
            self._show_image(path,8,32,x,y)
            ind=x+10
        elif d==2 or d==3:    
            self._show_image(path,18,32,x,y)
            ind=x+20
        else:
            self._show_image(path,19,32,x,y)
            ind=x+21
        d=int(n%10)
        path='bin/dig32/'+str(d)
        if d==1:
            self._show_image(path,8,32,ind,y)
        elif d==2 or d==3:    
            self._show_image(path,18,32,ind,y)
        else:
            self._show_image(path,19,32,ind,y)
    def show_logo(self):
        from time import sleep
        self.oled.fill(0)
        self._show_image('bin/icon/mush',32,32,48,0)
        self._show_image('bin/txt32/mush',110,24,9,34)
        self.oled.show()
        i=0
        sleep(2)
        while i<17:
            sleep(0.05)
            self.oled.scroll(0,-2)
            self.oled.show()
            i+=1
        self._show_image('bin/txt32/link',110,24,9,30)
        self.oled.show()
        git='0.0.1'
        try:
            with open('/app/.version') as f:
                    git = f.read()
        except OSError:
            git='0.0.1'
            pass            
        #from version import version
        sleep(2)    
        print('git ver==>',git)
        i=0
        while i<17:
            sleep(0.05)
            self.oled.scroll(0,-2)
            self.oled.show()
            i+=1
        self.oled.text(git,40,40)    
        self.oled.show()
        sleep(2)


    def _show_image(self,path,w,h,x,y):#show binary image
        try:
            f=open(path)
            s=f.read(int((w*h)/8))
            arr=bytearray(s)
            f.close()
            fbuf = framebuf.FrameBuffer(arr, w, h, framebuf.MONO_VLSB)
            self.oled.blit(fbuf,x,y)
        except OSError:
            pass
    def _show_err(self,n):
        self.oled.fill(0)
        path='bin/dig16/Err'
        self._show_image(path,33,16,30,24)     
        d=int(n%10)
        path='bin/dig16/'+str(d)
        self._show_image('bin/dig16/0',9,16,67,24)
        if d==1:
            self._show_image(path,4,16,79,24)
            
        elif d==2 or d==3:    
            self._show_image(path,9,16,79,24)
            
        else:
            self._show_image(path,9,16,79,24)
            
        
        self.oled.show()
    def set_err(self,n):
        self.enum=n
        if n!=0:
            self.err=True
            self.working=False
        else:
            self.err=False
            #print('resolved')

    def set_temp_hum(self,temp,hum):
        self.temp=temp
        self.hum=hum

    def _show_temp(self,t,h):
        self.oled.fill(0)
        self._show_num_32(t,0,0)
        self._show_image('bin/dig16/cg',20,16,43,0)
        self._show_image('bin/txt16/Fa/temp',25,16,100,5)
        self._show_num_32(h,0,32)
        self._show_image('bin/dig16/per',14,16,43,35)
        self._show_image('bin/txt16/Fa/hum',42,16,82,38)
        self.oled.show()    


    # def _show_hum(self,h):
    #     #print('hum',h)
    #     self.oled.fill(0)
    #     d=int(h/10)%10
    #     path='dgt/d'+str(d)
    #     if self.type!=2:
    #         self._show_image(path,26,40,20,5)
    #     else:    
    #         self._show_image(path,26,40,20,15)

    #     d=int(h%10)
    #     path='dgt/d'+str(d)
    #     if self.type!=2:
    #         self._show_image(path,26,40,48,5)
    #     else:
    #         self._show_image(path,26,40,48,15)

    #     if self.type!=2:
    #         self._show_image('app/percent.img',24,32,78,5)    
    #     else:
    #         self._show_image('app/percent.img',24,32,78,15)    
        
    #     self.oled.show()    

    def __init__(self,oled,wdt=None):
        self.wdt=wdt
        self.oled=oled
        self.err=False
        self.temp=25.0
        self.hum=55.0
        self.enum=0
        self.page=0
        self.item=0
    def show_menu(self,page,item):
        print('MENU:',page,item)
        if page==1:
            if self.item==3:
                if item==0:
                    self.sd=True

                if item==2:
                    self.su=True    

            if self.item==2:
                if item==3:
                    self.sd=True

                if item==1:
                    self.su=True            

            if self.item==1:
                if item==2:
                    self.sd=True
                if item==0:
                    self.su=True    
            if self.item==0:
                if item==1:
                    self.sd=True

                if item==3:
                    self.su=True    

        if self.page!=page:
            self.oled.fill(0)
            self.pchange=True
            self.su=False
            self.sd=False
        self.page=page
        self.item=item
        
        self.ichange=True
    def get_page(self):
        return self.page
    def get_item(self):
        return self.item
    async def Run(self):
        self.type=1
        cnt=0
        self.ichange=False
        self.pchange=False
        self.su=False
        self.sd=False
        while True:
            if self.page==0:
                if self.enum!=1:#if temp sensor has no error show hum and temp    
                    self._show_temp(self.temp,self.hum)    
                    await uasyncio.sleep_ms(2000)
                if self.err:
                    self._show_err(self.enum)    
                    await uasyncio.sleep_ms(2000)
                cnt+=1
            elif self.page==1:#menu
                if self.ichange:
                    self.ichange=False
                    if self.pchange:
                        self.pchange=False
                        self._show_image('bin/dig16/s',18,16,110,24) 
                        self._show_image('bin/txt16/Fa/upd',32,16,76,4) 
                        self._show_image('bin/txt16/Fa/temp',25,16,83,24)    
                        self._show_image('bin/txt16/Fa/hum',42,16,66,44)

                    if self.sd:
                        i=0
                        while i<5:
                            self.oled.fill_rect(110,24,22,16,0)   
                            self.oled.scroll(0,-4)
                            self._show_image('bin/dig16/s',18,16,110,24) 
                            i+=1
                            self.oled.show()
                        #print('sd')
                        self.sd=False
                        self.oled.fill_rect(66,44,42,16,0)   
                        if self.item==0:
                            self._show_image('bin/txt16/Fa/hum',42,16,66,44)
                        if self.item==1:
                            self._show_image('bin/txt16/Fa/fan',18,16,90,44) 
                        if self.item==2:
                            self._show_image('bin/txt16/Fa/upd',32,16,76,44)
                        if self.item==3:
                            self._show_image('bin/txt16/Fa/temp',25,16,83,44)    

                    
                    if self.su:
                        i=0
                        while i<5:
                            self.oled.fill_rect(110,24,22,16,0)   
                            self.oled.scroll(0,4)
                            self._show_image('bin/dig16/s',18,16,110,24) 
                            i+=1
                            self.oled.show()
                        #print('su')
                        self.su=False
                        self.oled.fill_rect(66,4,42,16,0)   
                        if self.item==0:
                            self._show_image('bin/txt16/Fa/upd',32,16,76,4) 
                        if self.item==1:
                            self._show_image('bin/txt16/Fa/temp',25,16,83,4)    
                        if self.item==2:
                            self._show_image('bin/txt16/Fa/hum',42,16,66,4)
                        if self.item==3:
                            self._show_image('bin/txt16/Fa/fan',18,16,90,4)     
                    self.oled.show()

            elif self.page==2:#menu
                if self.ichange:
                    if self.pchange:
                        self.pchange=False
                        self._show_image('bin/txt16/Fa/temp',25,16,83,0)    
                        self._show_image('bin/dig16/dd',5,16,74,3)    
                    self._show_num_32(self.item,30,32)
                    self._show_image('bin/dig16/cg',20,16,73,32)                        
                    self.oled.show()

            elif self.page==3:#menu
                if self.ichange:
                    if self.pchange:
                        self.pchange=False
                        #self._show_image('bin/txt16/Fa/temp',25,16,83,0)
                        self._show_image('bin/txt16/Fa/hum',42,16,82,0)    
                        self._show_image('bin/dig16/dd',5,16,74,3)    
                    self._show_num_32(self.item,30,32)
                    self._show_image('bin/dig16/per',14,16,73,32)                        
                    self.oled.show()                    
            elif self.page==4:
                if self.ichange:
                    self.ichange=False
                    if self.pchange:
                        self.pchange=False
                        self._show_image('bin/dig16/s',18,16,110,12) 
                        self._show_image('bin/txt16/Fa/time',28,16,80,12)    
                        self._show_image('bin/txt16/Fa/on',37,16,36,12)    
                        self._show_image('bin/txt16/Fa/time',28,16,80,32)
                        self._show_image('bin/txt16/Fa/off',49,16,20,32)
                        
                    else:
                        if self.item==0:
                            self._show_image('bin/dig16/s',18,16,110,12) 
                            self.oled.fill_rect(110,32,22,16,0)   
                        else:
                            self._show_image('bin/dig16/s',18,16,110,32)     
                            self.oled.fill_rect(110,12,22,16,0)   
                            
                    self.oled.show()                            

            elif self.page==40:
                if self.ichange:
                    self.ichange=False
                    if self.pchange:
                        self.pchange=False
                        self._show_image('bin/txt16/Fa/time',28,16,80,0)    
                        self._show_image('bin/txt16/Fa/on',37,16,40,0)    
                        self._show_image('bin/dig16/dd',5,16,35,3)    
                        self._show_num_32(self.item,30,32)
                    else:
                        self._show_num_32(self.item,30,32)
                    self.oled.show()                            
            elif self.page==41:
                if self.ichange:
                    self.ichange=False
                    if self.pchange:
                        self.pchange=False
                        self._show_image('bin/txt16/Fa/time',28,16,80,0)    
                        self._show_image('bin/txt16/Fa/off',49,16,20,0)    
                        self._show_image('bin/dig16/dd',5,16,15,3)    
                        self._show_num_32(self.item,30,32)
                    else:
                        self._show_num_32(self.item,30,32)
                    self.oled.show()                                
            if self.wdt!=None:                
                self.wdt.feed()
            await uasyncio.sleep_ms(300)

