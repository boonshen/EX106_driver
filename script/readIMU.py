#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import serial
import time
import binascii

port = '/dev/ttyACM0'
#IMUser = serial.Serial('/dev/ttyACM0',57600,timeout=0.025)#for linux
#IMUser = serial.Serial('/dev/tty.usbmodem1411',57600,timeout=0.025)#for mac
IMUser = serial.Serial(port, baudrate=57600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

def readData():
	data = ""
	while (IMUser.read() != '!'):#一直读直到遇到包头'!'
		pass#print(IMUser.read())
	ch = IMUser.read()
	while (ch != '*'):#一直读，读到一个char就加入data包，一直读到包尾'*'为止
		data += ch
		ch = IMUser.read()
	result = parseData(data)#将字符串改为一个list[roll,pitch,yaw]
	return result	#roll pitch yaw

def flush():
	IMUser.flushOutput()
	IMUser.flushInput()

def parseData(data):
	result = data.split(",")#包中数据的分隔符为',' 所以以逗号为分隔符将string分开
	for num in range(0,3):
		result[num] = float(result[num])#将string转化为float
	return result

if __name__ == '__main__':
	while True:
		pose = readData()
		print(pose)
