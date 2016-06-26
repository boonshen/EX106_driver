#Head包程序
---
上一版程序（当前master和old-master）：使用python的serial进行串口通信，对Dynamixel的EX106进行驱动。

最新版程序(ros分支)：使用python与arduino的serial进行通讯读取IMU，利用service驱动头部电机，并且发送msg给gait/head_pose


##Usage
---

	##旧版本，/dev/ttyUSB1为arduino串口，/dev/ttyUSB0为电机控制串口
	python head.py
	
	##新版本，在/catkin_ws/src下
	git clone git@github.com:guzhaoyuan/Head.git
	cd ..
	catkin_make
	rosrun Head head.py
	
##功能
---
-  node 为 /Head_data
	- 给 gait/head_angel 的 topic 发 msg
-  node 为 /head_control_server
	- 给 Head/head_servo_angel 的 topic 发 msg	
	- 提供 /head_control_withPID 的 service 控制头部电机

##Structure
---

- head2.py #新版主程序入口，从head.py修改而来
- head_client.py #控制头部电机的client
- head.py #主程序入口,PID控制电机保持某一姿态
- EX106.py #底层驱动，串口通讯
- pid.py #pid算法实现
- readIMU.py #读取IMU数据并且使用
- home.py #测试文件,用于将电机返回中值

##Dependency
---

- pySerial
- time

##ToDo
---

- 考虑PID的应用场景
- ~~和决策确定接口和PID使用方法~~
- ~~添加2个msg，分别为头部姿态和头部电机转角~~
- ~~给ROS添加 service~~
- ~~评估工作量修改底层驱动代码工作量~~
- ~~修改底层代码~~

