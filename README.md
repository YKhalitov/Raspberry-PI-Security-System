# Raspberry-PI-Security-System
Designed for a raspberry PI & several circuit components connected on a breadboard.
Connections made are detailed in documentation.

Allows user to enable/disable the system using the RFID card reader module.
An LED indicates the current state of the program.
The ultrasonic sensor detects changes in distance between it and the door frame
its attached to showing someone walked through.

In the event someone walks through with the alarm enabled the alarm system
will beep repeatedly.

Only the RFID card with the correct password can turn it off/on.
Correct Password = "Alex"


Need to use read & write file first to write the correct password to RFID card.

