from MX1508 import *
from time import sleep_ms
from machine import Pin, Timer
 
motor_L = MX1508(4, 2)
motor_R = MX1508(19, 18)
Sp=1023
R_W_count,L_W_count=0,0
while(1):
    motor_L.forward(Sp)
    motor_R.forward(Sp)