import webiopi
import subprocess
import os

webiopi.setDebug()

GPIO = webiopi.GPIO

PIN_L1 = 22
PIN_L2 = 23
PIN_R1 = 11
PIN_R2 = 9

g_mode = 0
g_percentage = 50

GPIO.setFunction( PIN_L1, GPIO.PWM )
GPIO.setFunction( PIN_L2, GPIO.PWM )
GPIO.setFunction( PIN_R1, GPIO.PWM )
GPIO.setFunction( PIN_R2, GPIO.PWM )

def MotorDrive( iIn1Pin, iIn2Pin, percentage ):
	if 100 < percentage:
		percentage = 100
	if -100 > percentage:
		percentage = -100
	if 10 > percentage and -10 < percentage:
		GPIO.pwmWrite( iIn1Pin, 0.0 )
		GPIO.pwmWrite( iIn2Pin, 0.0 )
	elif 0 < percentage:
		GPIO.pwmWrite( iIn1Pin, percentage * 0.01 )
		GPIO.pwmWrite( iIn2Pin, 0.0 )
	else:
		GPIO.pwmWrite( iIn1Pin, 0.0 )
		GPIO.pwmWrite( iIn2Pin, -percentage * 0.01 )

@webiopi.macro
def ChangeDriveMode( mode ):
	if mode == "0":
		webiopi.debug("ChangeDriveMode : Stop")
		MotorDrive( PIN_L1, PIN_L2, 0 );
		MotorDrive( PIN_R1, PIN_R2, 0 );
	elif mode == "1":
		webiopi.debug("ChangeDriveMode : Forward")
		MotorDrive( PIN_L1, PIN_L2, g_percentage );
		MotorDrive( PIN_R1, PIN_R2, g_percentage );
	elif mode == "2":
		webiopi.debug("ChangeDriveMode : Backward")
		MotorDrive( PIN_L1, PIN_L2, -g_percentage );
		MotorDrive( PIN_R1, PIN_R2, -g_percentage );
	elif mode == "3":
		webiopi.debug("ChangeDriveMode : CW")
		MotorDrive( PIN_L1, PIN_L2, g_percentage );
		MotorDrive( PIN_R1, PIN_R2, -g_percentage );
	elif mode == "4":
		webiopi.debug("ChangeDriveMode : CCW")
		MotorDrive( PIN_L1, PIN_L2, -g_percentage );
		MotorDrive( PIN_R1, PIN_R2, g_percentage );
	global g_mode
	g_mode = mode

@webiopi.macro
def ChangeVoltageLevel( level ):
	webiopi.debug("ChangeVoltageLevel : %s" % (level))
	global g_percentage
	g_percentage = 10 * int(level)
	ChangeDriveMode( g_mode )

@webiopi.macro
def SnapShot():
	webiopi.debug("getPic")
	cmd = "sh /home/pi/take_pic.sh"
	back = subprocess.call(cmd, shell=True)
	webiopi.debug(back)
	if back == 0:
		return "0"
	else:
		return "1"

@webiopi.macro
def InitPic():
	imageFiles = ""
	images = os.listdir('/home/pi/work/webiopi/images/')
	for image in images:
		imageFiles += image + ","
	return imageFiles