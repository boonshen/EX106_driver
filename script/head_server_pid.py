#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import time
import readIMU
import pid
import rospy
import head_client
from operator import add
from Head.msg import head_pose 
#from gait.msg import head_angle_msg
from Head.srv import head_control
from Head.msg import head_servo_angel


Pi = 3.1415926

#publish msg to head_servo_angel.msg 
pub_servo = rospy.Publisher('Head/head_servo_angel',head_servo_angel,queue_size=100)

#servo init angel
init_pitch = 0
init_yaw = 0

#当前的位置
#初始化时，当前位置等于初始位置
current_pitch = init_pitch
current_yaw = init_yaw

#callback function receive pitch[-Pi/2,Pi/2] and yaw[-Pi,Pi] and call security service directly
def handle_head_control(req):
	pitch = (req.pitch)
	yaw = (req.yaw)
	head_client.sync_write_angel_client(yaw,pitch,0)
	return 0

#server init, receive yaw and pitch
def head_control_server():
	rospy.init_node('head_control_server')
	s = rospy.Service('head_control_withPID',head_control,handle_head_control)
	print "head control server ready"
	rospy.spin()


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
	if (abs(current_pitch) < head_client.soft_limit):
		current_pitch -= offset[0]#修改pitch输出
	if (abs(current_yaw) < head_client.soft_limit):
		current_yaw -= offset[2]#修改yaw输出

	print("command yaw:"),
	print(current_yaw),
	print("command pitch"),
	print(current_pitch)
#	sync_write_angel(1,current_yaw,2,current_pitch)
	head_client.sync_write_angel_client(current_yaw,current_pitch,0)
	pub_servo.publish(current_pitch,current_yaw)
        #send servo pose every after servo move

#主函数
if __name__ == '__main__':
	head_control_server()	
