#! /usr/bin/env python
import rospy
from services_quiz.srv import ServiceMessage, ServiceMessageResponse
from math import sqrt
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import time, datetime


def my_callback(request):
    rospy.loginfo("The Service move_direction has been called")
    vel.linear.x = 0.1
    vel.angular.z = 0.0
    duration = request.duration
    start_time = rospy.get_time()
    while start_time + duration > rospy.get_time():
      if request.direction == 'forward' :
         ok = move_forward(0.2)
      elif request.direction == 'backward' :
         ok = move_backward(0.6)


    pub.publish(vel)
    rospy.loginfo("Finished service move_direction")

    response = ServiceMessageResponse()
    if not ok:
        print('Error! An obstacle was found.')
        response.complete = False
    else:
        response.complete = True

    return response  

def new_distance(init_pos):
    crt_odom = rospy.wait_for_message('/odom', Odometry, timeout=1)
    crt_position = crt_odom.pose.pose.position
    distance = sqrt((crt_position.x - init_pos.x) * (crt_position.x - init_pos.x) +
                   (crt_position.y - init_pos.y)*(crt_position.y - init_pos.y))
    return distance

def move_forward(dist):
    init_odom = rospy.wait_for_message('/odom', Odometry, timeout=1)
    init_position = init_odom.pose.pose.position
    ok = 1
    
    while dist > new_distance(init_position):
        pub.publish(vel)
    vel.linear.x = 0.0
    if ok: print('The robot moved straight for 15cm')
    return ok
    

def move_backward(dist):
    init_odom = rospy.wait_for_message('/odom', Odometry, timeout=1)
    init_position = init_odom.pose.pose.position
    ok = 1
    while dist > new_distance(init_position):
        vel.linear.x = -0.1
        pub.publish(vel)
    vel.linear.x = 0.0
    if ok: print('The robot moved backward for 15cm')
    return ok
    
    
    

rospy.init_node('turtlebot_move_service_server')

my_service = rospy.Service('/move_robot', ServiceMessage,
                           my_callback)
# Create a publisher to the topic /cmd_vel
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
vel = Twist()  # Create a var of type Twist
rate = rospy.Rate(1)
rospy.loginfo("Service /move_direction Ready")
rospy.spin()
