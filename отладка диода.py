from machine import Pin,I2C
from neopixel import NeoPixel
from MX1508 import *
from VL53L0X import *
from tcs34725 import *
from time import sleep_ms,sleep
import uasyncio as asio
import aioespnow
import network

i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
tcs = TCS34725(i2c_bus)
tcs.gain(4)#gain must be 1, 4, 16 or 60
tcs.integration_time(80)
i2c_bus1 = I2C(1, sda=Pin(21), scl=Pin(22))
tof = VL53L0X(i2c_bus1)

NUM_OF_LED = 1
np = NeoPixel(Pin(14), NUM_OF_LED)
color=['Red','Yellow','White','Green','Black','Cyan','Blue','Magenta']
dir_move=['Stop','Forward','Left','Right','Reverse']
motor_L = MX1508(2, 4)
motor_R = MX1508(19, 18)
Sp=900
Sp1=int(Sp*0.3)
Lt=60
alfa=0.8
debug=1

async def color_det():
    global col_id,col_id_l
    rgb=tcs.read(1)
    r,g,b=rgb[0],rgb[1],rgb[2]
    h,s,v=rgb_to_hsv(r,g,b)
    if 0<h<60:
        col_id_l=col_id
        col_id=0
    elif 61<h<120:
        col_id_l=col_id
        col_id=1
    elif 121<h<180:
        if v>100:
            col_id_l=col_id
            col_id=2
        elif 25<v<100:
            col_id_l=col_id
            col_id=3
        elif v<25:
            col_id_l=col_id
            col_id=4
    elif 181<h<240:
        if v>40:
            col_id_l=col_id
            col_id=5
        else:
            col_id_l=col_id
            col_id=6
    elif 241<h<360:
        col_id_l=col_id
        col_id=7 
    if debug:
        print('Color is {}. R:{} G:{} B:{} H:{:.0f} S:{:.0f} V:{:.0f}'.format(color[col_id],r,g,b,h,s,v))      

async def LED_cont(int_ms):
    while 1:
        await asio.sleep_ms(int_ms)
        if col_id==0:
            np[0]=(Lt,0,0)
        elif col_id==1:
            np[0]=(Lt,Lt,0)
        elif col_id==2:
            np[0]=(Lt,Lt,Lt)
        elif col_id==3:
            np[0]=(0,Lt,0)
        elif col_id==4:
            np[0]=(0,0,0)
            np.write()
            await asio.sleep_ms(300)
            np[0]=(Lt,0,0)
            np.write()
            await asio.sleep_ms(300)
        elif col_id==5:
            np[0]=(0,Lt,Lt)
        elif col_id==6:
            np[0]=(0,0,Lt) 
        elif col_id==7:
            np[0]=(Lt,0,Lt)
        if di==0:
            np[1]=(0,Lt,0)
        elif di==1:
            np[1]=(Lt,Lt,0)
        elif di==2:
            np[1]=(Lt,0,0)
        np.write()
        

# define loop
loop = asio.get_event_loop()

#create looped tasks


loop.create_task(LED_cont(100))

    

