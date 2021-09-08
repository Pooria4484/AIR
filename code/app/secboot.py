from save import load,save
from time import sleep
try:
    flag=load(b"update")
except KeyError:
    from save import save
    flag=b"False"
    save(b"update",flag)
print('update-->',flag) 


from machine import SoftI2C,Pin,freq
from oled import SSD1306_I2C
i2c = SoftI2C(scl=Pin(15), sda=Pin(13),freq=400000)
oled=SSD1306_I2C(128, 64, i2c, 0x3c,dir=False)
oled.fill(0)
freq(240000000)
print('fr-->',freq())

################################
flag=b"True"
save("link",'https://github.com/Pooria4484/AIR')
print(load("link").decode('utf-8'))
################################
if flag==b"True":
    oled.text('UPDATING',32,29)
    oled.show()
    sleep(2)
    oled.text('..',5,40)
    oled.show()
    sleep(1)
    oled.text('....',5,40)
    oled.show()
    sleep(1)
    oled.text('.......',5,40)
    oled.show()
    sleep(1)
    oled.text('.........',5,40)
    oled.show()
    import update
else:
    try:
        from .ui import UI
        ui=UI(oled)
        ui.show_logo()
        # from . version import version as app_ver
        # git=''
        # try:
        #     with open('/app/.version') as f:
        #             git = f.read()
        # except OSError:
        #     pass            
        # from version import version
        # print('build ver==>',version,'\n','app ver==>',app_ver)
        # print('git ver==>',git)
        # oled.text(git,40,40)    
    except ImportError:
        print('no release it is debug')
  