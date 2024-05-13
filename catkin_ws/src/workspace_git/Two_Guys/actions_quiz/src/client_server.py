#!/usr/bin/env python

import rospy
import actionlib
from action_quiz.msg import MyAction, MyActionGoal, MyActionFeedback, MyActionResult
from geometry_msgs.msg import Twist
from math import sin, cos


def client():
    rospy.init_node('circle_action_client')
    client = actionlib.SimpleActionClient('circle_action', MyAction)
    client.wait_for_server()

    goal = MyActionGoal()
    goal.seconds = 10  # Example: move in circle for 10 seconds

    client.send_goal(goal.goal_data)
    client.wait_for_result()

    result = client.get_result()
    rospy.loginfo("Final Orientation Y: {}".format(result.result_data[0]))


if _name_ == '_main_':
    try:
        client()
    except rospy.ROSInterruptException:
        pass
