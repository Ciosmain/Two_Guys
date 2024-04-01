#! /usr/bin/env python
import rospy
import time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def callback(msg):
   print ("mesaj")
    # Define a function called 'callback' that receives a parameter named 'msg'
   if msg.ranges[0] < 0.3:
#Stop turn right
     print("mesaj trimis: ")
     print(msg.ranges) 
     turn.linear.x = 0
     turn.linear.z = 0
     time.sleep(2)
     print ("mesaj 2")
   #  turn.angular.x = 0
     pub.publish(turn)
     turn.angular.x = 0.05
     turn.linear.z = 0
     pub.publish(turn)
     time.sleep(2)
     print ("mesaj 3")
     print ("mesaj 4")
     turn.angular.z = 1
     turn.linear.x = 0
     pub.publish(turn)
     print ("mesaj 5")
     time.sleep(2)
   #mergi inainte
   turn.linear.x = 2
   pub.publish(turn)
   print ("coordonata: ")
   print (msg.ranges[0])                            	# Print the value 'data' inside the 'msg' parameter

rospy.init_node('scan_subscriber')                   	# Initiate a Node called 'topic_subscriber'
sub = rospy.Subscriber('/scan', LaserScan, callback)   	# Create a Subscriber object that will listen to the /counter
pub = rospy.Publisher('/cmd_vel',Twist,queue_size=1)

#Trb completat                                                      			# topic and will call the 'callback' function each time it reads
rate = rospy.Rate(2)
turn = Twist()
                                                      			# something from the topic
rospy.spin()
