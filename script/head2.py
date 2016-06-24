#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#import EX106
import time
import readIMU
import pid
import rospy
import head_client
from operator import add
from Head.msg import head_pose 
#from gait.msg import head_angle_msg

pub = rospy.Publisher('gait/head_angle',head_pose)
rospy.init_node('IMU_data',anonymous=True)


#servo init angel
init_pitch = 0
init_yaw = 0

#当前的位置
#初始化时，当前位置等于初始位置
current_pitch = init_pitch
current_yaw = init_yaw

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
	head_client.sync_write_angel_client(current_yaw,current_pitch,0)

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

	#init head posion (0 , 0)
	head_client.sync_write_angel_client(init_yaw,init_pitch,0)

	for num in range(1,100): #读200组数据扔掉
		pose = readIMU.readData()
	
	target = get_average_IMU(10) #读10组数据做平均做出初始值
	
	while True:
		temp = get_average_IMU(2) #读4组数据做平均作为当前姿态
		pub.publish(head_pose(temp[2],temp[0]))
		readIMU.flush()
  		keep_position(target,temp)
