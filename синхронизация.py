from MX1508 import *
from time import sleep_ms
from machine import Pin, Timer

R_m_pin = Pin(32, Pin.IN)
L_m_pin = Pin(25, Pin.IN)

def R_W_int(pin):
    global R_W_count
    R_W_count+=1
    
def L_W_int(pin):
    global L_W_count
    L_W_count+=1
    
R_m_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler=R_W_int)
L_m_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler=L_W_int)

timer = Timer(0)

def W_sp(timer):
    global R_W_count, L_W_count,direct 
    if direct==0:
        if R_W_count>L_W_count:
            motor_R.forward(0)
            motor_L.forward(Sp)
        elif R_W_count<L_W_count:
            motor_R.forward(Sp)
            motor_L.forward(0)
        else:
            motor_R.forward(Sp)
            motor_L.forward(Sp)
    if direct==1:
        if R_W_count>L_W_count:
            motor_R.forward(0)
            motor_L.reverse(Sp)
        elif R_W_count<L_W_count:
            motor_R.forward(Sp)
            motor_L.reverse(0)
        else:
            motor_R.forward(Sp)
            motor_L.reverse(Sp)
    if direct==2:
        if R_W_count>L_W_count:
            motor_R.reverse(0)
            motor_L.forward(Sp)
        elif R_W_count<L_W_count:
            motor_R.reverse(Sp)
            motor_L.forward(0)
        else:
            motor_R.reverse(Sp)
            motor_L.forward(Sp)
    if direct==3:
        if R_W_count>L_W_count:
            motor_R.reverse(0)
            motor_L.reverse(Sp)
        elif R_W_count<L_W_count:
            motor_R.reverse(Sp)
            motor_L.reverse(0)
        else:
            motor_R.reverse(Sp)
            motor_L.reverse(Sp)
            
timer.init(period=1, mode=Timer.PERIODIC, callback=W_sp)

motor_L = MX1508(2, 4)
motor_R = MX1508(19, 18)
Sp=512
R_W_count,L_W_count,direct=0,0,0 
while(1):
    print(R_W_count,L_W_count)
    sleep_ms(200)
          