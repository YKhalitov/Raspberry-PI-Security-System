# *****************************************************************************
# ***************************  Python Source Code  ****************************
# *****************************************************************************
# 
#   DESIGNER NAME:  Yaroslav Khalitov
#  
#       FILE NAME:  Final Project
#  
#            DATE:  11/24/2021
#
# DESCRIPTION
#  Final Project Description
#
# *****************************************************************************

# modules used by this file
import time
import threading
import concurrent.futures
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

#---------------------------------------------------
# Global constants to be used in program
#--------------------------------------------------

#RFID reader
reader = SimpleMFRC522()

#PWM frequency
FREQUENCY = 2000

#time delays
TIME_DELAY_1US = 0.000001
TIME_DELAY_10US = 0.00001

TIME_DELAY_10000MS = 10.0
TIME_DELAY_2250MS = 2.25
TIME_DELAY_700MS = 0.70
TIME_DELAY_600MS = 0.60
TIME_DELAY_500MS = 0.50
TIME_DELAY_250MS = 0.25
TIME_DELAY_150MS = 0.15
TIME_DELAY_100MS = 0.10
TIME_DELAY_50MS = 0.05

#calculating distance
ONE_WAY = 2
REPEAT_TIMES = 10
US_TO_SEC = 10000
MICRO_TO_SEC = 1000000
SOUND_SPEED = 340
MAX_DISTANCE = 220
timeOut = MAX_DISTANCE * 60

#distance error buffer
BUFFER_DISTANCE_POS = 5
BUFFER_DISTANCE_NEG = -5

#passwords
CORRECT_PASSWORD = "Alex"
DEFAULT_PASSWORD = "default"

#light values
RGB_RED = [0, 100, 100]
RGB_GREEN = [100, 0, 100]
RGB_ORANGE = [0, 35, 100]
RGB_OFF = [100, 100, 100]
RED_INDEX = 0
GREEN_INDEX = 1
BLUE_INDEX = 2

#---------------------------------------------------
# Pins
#---------------------------------------------------

#ultrasonic sensor
trigPin = 16
echoPin = 18
buzzerPin = 7

#RGB LED
LED_RED = 29 
LED_GREEN = 31
LED_BLUE = 37



# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will set up the GPIO pins
#
# INPUT PARAMETERS:
#   none
#
# OUTPUT PARAMETERS:
#   none
#
# RETURN:
#   none
#
# -----------------------------------------------------------------------------
def setup_gpio():
    global pRED
    global pGREEN
    global pBLUE
    
    # set up GPIO
    GPIO.setup(trigPin, GPIO.OUT)
    GPIO.setup(buzzerPin, GPIO.OUT)
    GPIO.setup(echoPin, GPIO.IN)
    
    # set intial out
    GPIO.output(buzzerPin, GPIO.LOW)
    
    # set up LEDs & p
    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.output(LED_RED, GPIO.HIGH)
  
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.output(LED_GREEN, GPIO.HIGH)
  
    GPIO.setup(LED_BLUE, GPIO.OUT)
    GPIO.output(LED_BLUE, GPIO.HIGH)
  
    pRED = GPIO.PWM(LED_RED, FREQUENCY)
    pGREEN = GPIO.PWM(LED_GREEN, FREQUENCY)
    pBLUE = GPIO.PWM(LED_BLUE, FREQUENCY)
  
    #start pwm
    pRED.start(RGB_OFF[RED_INDEX])
    pGREEN.start(RGB_OFF[GREEN_INDEX])
    pBLUE.start(RGB_OFF[BLUE_INDEX])
    


# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will send out a pulse and calculate the time it took to
#   come back.
#
# INPUT PARAMETERS:
#   pin - The pin number for the echo pin
#   level - A high GPIO output
#   timeout - The calculated timeout in US
#
# OUTPUT PARAMETERS:
#   none
#
# RETURN:
#   pulseTime - How long the ultrasonic sensor pulsed for
#
# -----------------------------------------------------------------------------
def send_trigger_pulse(pin, level, timeOut):
  begTime = time.time()
  while(GPIO.input(pin) != level):
      if((time.time() - begTime) > timeOut * TIME_DELAY_1US):
          return 0
        
  begTime = time.time()
  while(GPIO.input(pin) == level):
      if((time.time() - begTime) > timeOut * TIME_DELAY_1US):
          return 0
  
  #calculate pulse time
  pulseTime = (time.time() - begTime) * MICRO_TO_SEC
  

  return pulseTime 




# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will calculate the distance based on the time from the sensor
#
# INPUT PARAMETERS:
#   none
#
# OUTPUT PARAMETERS:
#   none
#
# RETURN:
#   distance - distance in cm between the sensor and object
#
# -----------------------------------------------------------------------------
def measure_return_echo():
  global distance
  while not quit:  
      GPIO.output(trigPin, GPIO.HIGH)  
      time.sleep(TIME_DELAY_10US)
      GPIO.output(trigPin, GPIO.LOW)
      
      pingTime = send_trigger_pulse(echoPin, GPIO.HIGH, timeOut)
      if pingTime == 0:
          print("ERROR: Missed pulse detection\n")
      
      distance = pingTime * SOUND_SPEED/ONE_WAY/US_TO_SEC
      time.sleep(TIME_DELAY_600MS)
  

  #return distance


# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will activate a warning if the distance is too short
#
# INPUT PARAMETERS:
#   none
#
# OUTPUT PARAMETERS:
#   none
#
# RETURN:
#   none
#
# -----------------------------------------------------------------------------
def activate_warning(pin, on_time):
    GPIO.output(buzzerPin, GPIO.HIGH)
    time.sleep(on_time)
    GPIO.output(buzzerPin, GPIO.LOW)
    
     
     
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will read RFID card
#
# INPUT PARAMETERS:
#   none
#
# OUTPUT PARAMETERS:
#   none
#
# RETURN:
#   none
#
# -----------------------------------------------------------------------------
def read():
    global password
    password = DEFAULT_PASSWORD
    while not quit:
        try:
              id, password = reader.read()
        except:
              print("Reading Error")
        finally:
              time.sleep(TIME_DELAY_700MS)
 
    

# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will change the LED
#
# INPUT PARAMETERS:
#   none
#
# OUTPUT PARAMETERS:
#   none
#
# RETURN:
#   none
#
# -----------------------------------------------------------------------------
def change_led_light(red, green, blue):
    pRED.ChangeDutyCycle(red)
    pGREEN.ChangeDutyCycle(green)
    pBLUE.ChangeDutyCycle(blue)
    
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will flash orange LED
#
# INPUT PARAMETERS:
#   none
#
# OUTPUT PARAMETERS:
#   none
#
# RETURN:
#   none
#
# -----------------------------------------------------------------------------
def flashing_orange_LED(red, green, blue):
    global flashingOrangeQuit
    
    while not quit:
        if not flashingOrangeQuit:
            change_led_light(red, green, blue)
            time.sleep(TIME_DELAY_100MS)
            change_led_light(RGB_OFF[RED_INDEX], RGB_OFF[GREEN_INDEX], RGB_OFF[BLUE_INDEX])
            time.sleep(TIME_DELAY_50MS)
            change_led_light(red, green, blue)
            time.sleep(TIME_DELAY_100MS)
            change_led_light(RGB_OFF[RED_INDEX], RGB_OFF[GREEN_INDEX], RGB_OFF[BLUE_INDEX])
            time.sleep(TIME_DELAY_2250MS)
        else:
            time.sleep(TIME_DELAY_700MS)
    
    
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will flash red LED
#
# INPUT PARAMETERS:
#   none
#
# OUTPUT PARAMETERS:
#   none
#
# RETURN:
#   none
#
# -----------------------------------------------------------------------------
def flashing_red_LED(red, green, blue):
    global flashingRedQuit
    
    while not quit:
        if not flashingRedQuit:
            change_led_light(red, green, blue)
            time.sleep(TIME_DELAY_100MS)
            change_led_light(RGB_OFF[RED_INDEX], RGB_OFF[GREEN_INDEX], RGB_OFF[BLUE_INDEX])
            time.sleep(TIME_DELAY_50MS)
            change_led_light(red, green, blue)
            time.sleep(TIME_DELAY_100MS)
            change_led_light(RGB_OFF[RED_INDEX], RGB_OFF[GREEN_INDEX], RGB_OFF[BLUE_INDEX])
            time.sleep(TIME_DELAY_2250MS)
        else:
            time.sleep(TIME_DELAY_700MS)


# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will loop and print the distance every second
#
# INPUT PARAMETERS:
#   none
#
# OUTPUT PARAMETERS:
#   none
#
# RETURN:
#   none
#
# -----------------------------------------------------------------------------
def loop(defaultAlarmDistance):
    global password
    global flashingOrangeQuit
    global flashingRedQuit
    
    #default states
    setState = True
    waitState = False
    panicState = False
    flashingOrangeQuit = True
    flashingRedQuit = True
    
    #variable to flash orange light in waitState
    doOnce = 0
    
    #main while loop
    while not quit:
        #get rid of /n characters
        password = password.strip()
        
        #--------------------------------------
        #***************SET STATE**************
        #--------------------------------------
        if setState:
            print("Set")
            #constant orange light
            change_led_light(RGB_ORANGE[RED_INDEX], RGB_ORANGE[GREEN_INDEX], RGB_ORANGE[BLUE_INDEX])
            
            #check for password
            if password == CORRECT_PASSWORD:
                #green light and buzzer
                change_led_light(RGB_GREEN[RED_INDEX], RGB_GREEN[GREEN_INDEX], RGB_GREEN[BLUE_INDEX])
                activate_warning(buzzerPin, TIME_DELAY_500MS)
                
                #change states
                setState = False
                waitState = True
                panicState = False
            elif password != CORRECT_PASSWORD and password != DEFAULT_PASSWORD:
                #red light and buzzer
                change_led_light(RGB_RED[RED_INDEX], RGB_RED[GREEN_INDEX], RGB_RED[BLUE_INDEX])
                activate_warning(buzzerPin, TIME_DELAY_500MS)

            
            
        #--------------------------------------
        #**************WAIT STATE**************
        #--------------------------------------       
        elif waitState:
            print("Wait")
            
            #turn on orange delay for 10 seconds
            if doOnce == 0:
                flashingOrangeQuit = False
                time.sleep(TIME_DELAY_10000MS)
                flashingOrangeQuit = True
                doOnce = 1
            
            #turn on flashing red light
            flashingRedQuit = False
                
            #check for distance change (someone walks through)
            if not BUFFER_DISTANCE_NEG <= (defaultAlarmDistance - distance) <= BUFFER_DISTANCE_POS:
                setState = False
                waitState = False
                panicState = True
                flashingRedQuit = True
                doOnce = 0
            
            #check for password
            if password == CORRECT_PASSWORD:
                #turn off flashing red LED
                flashingRedQuit = True
                
                #green light and buzzer
                change_led_light(RGB_GREEN[RED_INDEX], RGB_GREEN[GREEN_INDEX], RGB_GREEN[BLUE_INDEX])
                activate_warning(buzzerPin, TIME_DELAY_500MS)
                
                #change states
                setState = True
                waitState = False
                panicState = False
                doOnce = 0
                
            elif password != CORRECT_PASSWORD and password != DEFAULT_PASSWORD:
                #turn off flashing red LED
                flashingRedQuit = True
                
                #red light and buzzer
                change_led_light(RGB_RED[RED_INDEX], RGB_RED[GREEN_INDEX], RGB_RED[BLUE_INDEX])
                activate_warning(buzzerPin, TIME_DELAY_500MS)
                
                #turn on flashing red LED
                flashingRedQuit = False
                
          
          
        #--------------------------------------
        #**************PANIC STATE*************
        #--------------------------------------    
        elif panicState:
            print("Panic")
            while panicState:
                #constant red light
                change_led_light(RGB_RED[RED_INDEX], RGB_RED[GREEN_INDEX], RGB_RED[BLUE_INDEX])
                
                #buzzer alarm
                GPIO.output(buzzerPin, GPIO.HIGH)
                time.sleep(TIME_DELAY_150MS)
                GPIO.output(buzzerPin, GPIO.LOW)
                time.sleep(TIME_DELAY_150MS)
                
                #check for password
                password = password.strip()
                if password == CORRECT_PASSWORD:
                    #green light and buzzer
                    change_led_light(RGB_GREEN[RED_INDEX], RGB_GREEN[GREEN_INDEX], RGB_GREEN[BLUE_INDEX])
                    activate_warning(buzzerPin, TIME_DELAY_500MS)
                    
                    #change states
                    setState = True
                    waitState = False
                    panicState = False

        
        
        #debug
        print(password)
        print(defaultAlarmDistance)
        print(distance)
        print("\n")
        
        #resets password
        password = DEFAULT_PASSWORD
        time.sleep(TIME_DELAY_700MS) 

     
  

#---------------------------------------------------------------------
# main function of program
#---------------------------------------------------------------------
def main():
  global quit
  quit = False  
  try:
    print("**Starting**")
    print("**Press CTRL-C To Terminate*")
    setup_gpio()
 
    #get default distance
    GPIO.output(trigPin, GPIO.HIGH)  
    time.sleep(TIME_DELAY_10US)
    GPIO.output(trigPin, GPIO.LOW)
    pingTime = send_trigger_pulse(echoPin, GPIO.HIGH, timeOut)
    if pingTime == 0:
      print("ERROR: Missed pulse detection\n")
    defaultAlarmDistance = pingTime * SOUND_SPEED/ONE_WAY/US_TO_SEC

    #start threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
      readerThread = executor.submit(read)
      distanceThread = executor.submit(measure_return_echo)
      mainLoopThread = executor.submit(loop, defaultAlarmDistance)
      flashingOrangeThread = executor.submit(flashing_orange_LED, RGB_ORANGE[RED_INDEX], RGB_ORANGE[GREEN_INDEX], RGB_ORANGE[BLUE_INDEX])
      flashingRedThread = executor.submit(flashing_red_LED, RGB_RED[RED_INDEX], RGB_RED[GREEN_INDEX], RGB_RED[BLUE_INDEX])
                   
    
  except KeyboardInterrupt:
    quit = True
    print("**TERMINATED**")
  except:
    print("**ERROR**")
  finally:
    pRED.stop()
    pGREEN.stop()
    pBLUE.stop()
    GPIO.cleanup()
    print("**ENDING**")




# Call the main function.
if __name__ == '__main__':
  main()