# -*- coding: utf-8 -*- 
import time

Kp = 0.1
Kd = 0.01
Ki = 0.005

pre_err_pitch = 0
pre_err_yaw = 0
integral_pitch = 0
integral_yaw = 0

threshold = 3

start_time = time.time()
last_time = start_time

def calc_pid(target,pose):
	output = [0,0,0]
	
	global pre_err_pitch,pre_err_yaw,integral_pitch,integral_yaw,last_time
	
	current_time = time.time()#获得系统当前时间
	dt = current_time - last_time#更新时间差
	
	err_pitch = target[1] - pose[1]#计算差距
	err_yaw = target[2] - pose[2]#计算差距
	
	if(abs(err_pitch)>threshold):#如果差距大于阈值，则加入积分
		integral_pitch += err_pitch * dt
	if(abs(err_yaw)>threshold):#如果差距大于阈值，则加入积分
		integral_yaw += err_yaw * dt
	
	derivative_pitch = (err_pitch - pre_err_pitch)/dt #计算微分
	derivative_yaw = (err_yaw - pre_err_yaw)/dt #计算微分
	
	output[1] = Kp * err_pitch + Ki * integral_pitch + Kd * derivative_pitch #计算输出的偏移量
	output[2] = Kp * err_yaw + Ki * integral_yaw + Kd * derivative_yaw #计算输出的偏移量
	
	pre_err_pitch = err_pitch #更新差值
	pre_err_yaw = err_yaw #更新差值
	
	last_time = current_time#更新时间
	
	return output
