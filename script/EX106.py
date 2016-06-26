# -*- coding: utf-8 -*- 
import serial
import time
import binascii



port = '/dev/ttyUSB0'
#port = '/dev/tty.wchusbserial1420' #for Mac
ser = serial.Serial(port, baudrate=57600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,timeout=0.025,write_timeout=0.025)


def checksum(data):
    data = 0xFF & data
    crc = ~(data)

    if (crc <= 0x0F):
        crc = crc & 0xFF
    #print "crc= "+str(int(crc))
    return crc

def parse(respond):
	pack= binascii.hexlify(respond) 
	if pack[0:2] == '00':
		pack = pack[2:]
	if pack[0:2] != 'ff':
		return ''
	if pack[2:4] == 'ff':
		return [pack[4:6],pack[8:10]]#[id , error]
	else:
		return [pack[2:4],pack[6:8]]

def scan():
	ids = []
	for num in range(1,5):
		if ping(num) != None:
			ids.append(num)
	print "find id:"+str(ids)

def ping(id):
	print "ping id: %d" %id
	total = id +3
	crc = checksum(total)
	data =[id,2,1]
	data.append(crc)
	package = "".join(map(chr,[0xFF,0xFF] + data))
	ser.flushOutput();
	time.sleep(0.1)
	ser.write(package)
	respond = ser.read(size=7)
	result = parse(respond)
	if result != '':
		print "find motor id: %d"%id
		return id

def write(id,instr,*para):
	paras = list(para)
	total = id + len(paras) + 2 + instr + sum(paras)
	crc = checksum(total)
	data =[id,len(paras)+2,instr]
	data += paras
	data.append(crc)
	package = "".join(map(chr,[0xFF,0xFF] + data))
	ser.flushOutput();
	time.sleep(0.1)
	ser.write(package)
	respond = ser.read(size=7)
	result = parse(respond)

#command for each dynamixel is the same but param imput is not same
#servo = [id ,position&0xFF,position>>8,speed&0xFF,speed>>8]
def syncWrite(addressToWrite,*servoList):
	servoLists = list(servoList)
	data = [0XFE,len(servoLists)*len(servoLists[0])+4,0x83,addressToWrite,len(servoLists[0])-1]
	for num in servoLists:
		data += num	
	total = sum(data)
	crc = checksum(total)
	data.append(crc)
	package = "".join(map(chr,[0xFF,0xFF] + data))
	ser.flushOutput();
	time.sleep(0.1)
	ser.write(package)

#ser.flushOutput()
#ser.flushInput()
