from machine import SoftI2C,Pin,ADC,RTC,Timer,WDT
from oled import SSD1306_I2C
t1=Pin(33,Pin.IN)
t2=Pin(25,Pin.IN)
t3=Pin(26,Pin.IN)
t4=Pin(27,Pin.IN)
co=Pin(35,Pin.IN)
cooler_water=Pin(5,Pin.OUT)
cooler_motor=Pin(18,Pin.OUT)
cooler_speed=Pin(17,Pin.OUT)
buzz=Pin(16,Pin.OUT)
i2c = SoftI2C(scl=Pin(15), sda=Pin(13),freq=400000)
oled=SSD1306_I2C(128, 64, i2c, 0x3c,dir=False)
oled.fill(0)
rtc=RTC()

