#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import EX106
import time
import readIMU
import pid
import rospy
import head_client
from operator import add
from beginner_tutorials.msg import head_pose 
from gait.msg import head_angle_msg

pub = rospy.Publisher('gait/head_angle',head_pose)
rospy.init_node('IMU_data',anonymous=True)


servo1max = 3575
servo1min = 711
servo2max = 3072
servo2min = 113

#servo init angel
init_pitch = 0
init_yaw = 0

#当前的位置
#初始化时，当前位置等于初始位置
current_pitch = init_pitch
current_yaw = init_yaw

#输入0-208.6°，中间值为104.3°;输出0-0xFFF，中间值为0x800
def angelToPosition(angel):
	return int(angel*0xFFF/208.6)

#将电机的数据直接转化为sync_write可以读的格式
def generate_servo(id,position,speed = 0x200):
	return [id ,position&0xFF,position>>8,speed&0xFF,speed>>8]

#给单个电机写一个位置，位置表示为数值
def write_goal(id, position, speed = 0x200):
	if id == 1:
		if position > servo1max:
			position = servo1max
			print "exceed servo1 max"
		elif position < servo1min:
			position = servo1min
			print "exceed servo1 min"
	elif id == 2:
		if position > servo2max:
			position = servo2max
			print "exceed servo2 max"
		elif position < servo2min:
			position = servo2min
			print "exceed servo2 min"
	servo = generate_servo(id,position,speed)
	EX106.syncWrite(0x1E,servo)

#该函数用来控制2个电机，速度默认为0x40较慢，可以直接给两个电机写位置,前提是不超出电机转动范围
def sync_write_goal(id1,position1,id2,position2,speed1=0x200,speed2=0x200):
	servo1 = 0
	servo2 = 0
	#软限位防止角度过大
	if position1 > servo1max:
		position1 = servo1max
		print "exceed servo1 max"
	elif position1 < servo1min:
		position1 = servo1min
		print "exceed servo1 min"
	else:
		servo1 = generate_servo(id1,position1,speed1)
	#软限位防止角度过大
	if position2 > servo2max:
		position2 = servo2max
		print "exceed servo2 max"
	elif position2 < servo2min:
		position2 = servo2min
		print "exceed servo2 min"
	else:
		servo2 = generate_servo(id2,position2,speed2)
	#如果两个角度都在合理范围内，则转动电机到目标位置
	if ((servo1 != 0) and (servo2 != 0)):
		EX106.syncWrite(0x1E,servo1,servo2)#EX106.py中的底层连写函数


#将电机的位置封装为角度，中值为104.3°
def sync_write_angel(id1,angel1,id2,angel2,speed1=0x200,speed2=0x200):
	sync_write_goal(id1,angelToPosition(angel1),id2,angelToPosition(angel2),speed1,speed2)

#该函数用于保持头部平衡
def keep_position(target,pose):
	print("target= "),
	print(target),
	print("pose= "),
	print(pose)
	if abs(pose[0] - target[0])< 3:
		pitchAdd = 0
	else:
		pitchAdd = target[0] - pose[0]
	if abs(pose[2] - target[2])< 3:
		yawAdd = 0
	else:
		yawAdd = target[2] - pose[2]

	global current_pitch
	global current_yaw
	offset = pid.calc_pid(target,pose)#得到输出的偏移值
	print(offset)
	if (current_pitch < servo2max) and (current_pitch > servo2min):
		current_pitch -= offset[0]#修改pitch输出
	if (current_pitch < servo1max) and (current_pitch > servo1min):
		current_yaw -= offset[2]#修改yaw输出

	print("command yaw:"),
	print(current_yaw),
	print("command pitch"),
	print(current_pitch)
#	sync_write_angel(1,current_yaw,2,current_pitch)

#读num组数据做平均做出初始值
def get_average_IMU(num):
	pose = [0,0,0]
	for num in range(1,num+1):
		pose = map(add, pose, readIMU.readData())
	pose[:] = [x / num for x in pose]
	return pose

#主函数
if __name__ == '__main__':
	target = [0,0,0]#pitch roll yaw,其中roll没用

	#EX106.syncWrite(0x1E,generate_servo(1,init_pitch),generate_servo(2,init_yaw))
	#sync_write_angel(1,init_yaw,2,init_pitch)
	head_client.sync_write_angel_client(init_yaw,init_pitch,0)

	for num in range(1,100): #读200组数据扔掉
		pose = readIMU.readData()
	
	target = get_average_IMU(10) #读10组数据做平均做出初始值
	
	while True:
		temp = get_average_IMU(2) #读4组数据做平均作为当前姿态
		pub.publish(head_pose(temp[2],temp[0]))
		readIMU.flush()
  		keep_position(target,temp)
