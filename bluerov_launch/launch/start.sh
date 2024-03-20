#set the ros master IP
export ROS_HOSTNAME=192.168.2.8
export ROS_MASTER_URI=http://192.168.2.8:11311

#source the argonaut catkin workspace
source rov_ws/devel/setup.bash

#launch the system
roslaunch bluerov_launch bluerov_launch.launch
