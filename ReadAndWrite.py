# *****************************************************************************
# ***************************  Python Source Code  ****************************
# *****************************************************************************
# 
#   DESIGNER NAME:  Yaroslav Khalitov
# 
#       FILE NAME:  ReadAndWrite.py
#  
#            DATE:  11/24/2021
#
# DESCRIPTION
#  Read and write to RFID tag.
#
# *****************************************************************************

# modules used by this file
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

#---------------------------------------------------
# Global constants to be used in program
#--------------------------------------------------
reader = SimpleMFRC522()





# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will write to RFID card
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
def write():
    try:
        text = input("New Data: ")
        print ("Place Your Tag To Write")
        reader.write(text)
        print("Written")
    finally:
        return
        
    
    
    


# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will read the RFID card.
#   
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
    try:
        print ("Place Your Tag To Read")
        id, text = reader.read()
        print (id)
        print (text)
    finally:
        return
    
    
    
  





# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will get users input 
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
def loop():
  running = True
  userChoice = 0
  while running == True:
      userChoice = int(input("\n(1) Write \n(2) Read \n(3) Exit \n"))
      if userChoice == 1:
          write()
      elif userChoice == 2:
          read()
      elif userChoice == 3:
          running = False

      
      
      
      
  


#---------------------------------------------------------------------
# main function of program
#---------------------------------------------------------------------
def main():
  try:
    print("**Starting**")
    print("**Press CTRL-C To Terminate*")
    loop()
  except KeyboardInterrupt:
    print("**TERMINATED**")
  except:
    print("**ERROR**")
  finally:
    GPIO.cleanup()
    print("**ENDING**")




# Call the main function.
if __name__ == '__main__':
  main()