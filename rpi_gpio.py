import RPi.GPIO as GPIO
from time import sleep

# GPIO Pin
STEP11 = 0
STEP12 = 0
STEP13 = 0
STEP14 = 0
STEP21 = 0
STEP22 = 0
STEP23 = 0
STEP24 = 0
STEP31 = 0
STEP32 = 0
STEP33 = 0
STEP34 = 0
STEP41 = 0
STEP42 = 0
STEP43 = 0
STEP44 = 0
STEP51 = 0
STEP52 = 0
STEP53 = 0
STEP54 = 0
LED1 = 24
LED2 = 25
LED3 = 26
CW = 1
CCW = 0
SPR = 48  # Steps per rev (360/7.5)

# Set GPIO Pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP11, GPIO.OUT)
GPIO.setup(STEP12, GPIO.OUT)
GPIO.setup(STEP13, GPIO.OUT)
GPIO.setup(STEP14, GPIO.OUT)

GPIO.setup(STEP21, GPIO.OUT)
GPIO.setup(STEP22, GPIO.OUT)
GPIO.setup(STEP23, GPIO.OUT)
GPIO.setup(STEP24, GPIO.OUT)

GPIO.setup(STEP31, GPIO.OUT)
GPIO.setup(STEP32, GPIO.OUT)
GPIO.setup(STEP33, GPIO.OUT)
GPIO.setup(STEP34, GPIO.OUT)

GPIO.setup(STEP41, GPIO.OUT)
GPIO.setup(STEP42, GPIO.OUT)
GPIO.setup(STEP43, GPIO.OUT)
GPIO.setup(STEP44, GPIO.OUT)

GPIO.setup(STEP51, GPIO.OUT)
GPIO.setup(STEP52, GPIO.OUT)
GPIO.setup(STEP53, GPIO.OUT)
GPIO.setup(STEP54, GPIO.OUT)

GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED2,GPIO.OUT)
GPIO.setup(LED3,GPIO.OUT)

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
delay = 0.002

GPIO.output( STEP11, GPIO.LOW )
GPIO.output( STEP12, GPIO.LOW )
GPIO.output( STEP13, GPIO.LOW )
GPIO.output( STEP14, GPIO.LOW )

GPIO.output( STEP21, GPIO.LOW )
GPIO.output( STEP22, GPIO.LOW )
GPIO.output( STEP23, GPIO.LOW )
GPIO.output( STEP24, GPIO.LOW )

GPIO.output( STEP31, GPIO.LOW )
GPIO.output( STEP32, GPIO.LOW )
GPIO.output( STEP33, GPIO.LOW )
GPIO.output( STEP34, GPIO.LOW )

GPIO.output( STEP41, GPIO.LOW )
GPIO.output( STEP42, GPIO.LOW )
GPIO.output( STEP43, GPIO.LOW )
GPIO.output( STEP44, GPIO.LOW )

GPIO.output( STEP51, GPIO.LOW )
GPIO.output( STEP52, GPIO.LOW )
GPIO.output( STEP53, GPIO.LOW )
GPIO.output( STEP54, GPIO.LOW )

steps1 = [STEP11, STEP12, STEP13, STEP14]
steps2 = [STEP21, STEP22, STEP23, STEP24]
steps3 = [STEP31, STEP32, STEP33, STEP34]
steps4 = [STEP41, STEP42, STEP43, STEP44]
steps5 = [STEP51, STEP52, STEP53, STEP54]

motor_step_counter = 0

def motor_1rev(step):
    step_pin = [steps1, steps2, steps3, steps4, steps5]
    for i in range(step_count):
        for pin in range(0,len(step_pin[step])):
            GPIO.output(step_pin[step][pin],step_sequence[motor_step_counter][pin])
            motor_step_counter = (motor_step_counter-1)%8
            sleep(delay)

def set_led(led,state):
    GPIO.output(led,state)