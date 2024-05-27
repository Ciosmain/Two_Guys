#! /usr/bin/env python
import time
import rospy
import actionlib
from geometry_msgs.msg import Twist
from actions_quiz.msg import nameAction, nameGoal, nameResult, nameFeedback

def feedback_callback(feedback):
	turn = Twist()
	while client.get_state() < 2:
		#robot se misca in cerc
		turn.linear.x = 0.5
		turn.linear.z = 0.3
		pub.publish(turn)
		rate.sleep()
		
	if client.get_state() > 2:
		turn.linear.x = 0
		turn.linear.z = 0
		rate.sleep()


rospy.init_node('quiz_action_client')
client = actionlib.SimpleActionClient('/quiz_as', nameAction)
client.wait_for_server()

goal = nameGoal()
goal.duration = 15

client.send_goal(goal, feedback_cb = feedback_callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(2)
rospy.spin()

client.wait_for_result()
