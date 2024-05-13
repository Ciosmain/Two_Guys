#!/usr/bin/env python

import rospy
import actionlib
from actions_quiz.msg import MyAction, MyActionFeedback, MyActionResult
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import sin, cos


class CircleActionServer:
    def _init_(self):
        self.server = actionlib.SimpleActionServer('circle_action', MyAction, self.execute, False)
        self.server.start()

        self.pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.sub_odom = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.orientation_y = 0.0

    def odom_callback(self, msg):
        self.orientation_y = msg.pose.pose.orientation.y

    def execute(self, goal):
        angular_speed = 0.5  # radians per second
        linear_speed = 0.2   # meters per second
        rate = rospy.Rate(10)

        success = True
        feedback = MyActionFeedback()
        result = MyActionResult()

        start_time = rospy.Time.now()
        while (rospy.Time.now() - start_time).to_sec() < goal.seconds:
            cmd_vel = Twist()
            cmd_vel.linear.x = linear_speed
            cmd_vel.angular.z = angular_speed
            self.pub_cmd_vel.publish(cmd_vel)

            # Update feedback
            feedback.feedback_data = [self.orientation_y]
            self.server.publish_feedback(feedback)

            rate.sleep()

        # Stop robot
        self.pub_cmd_vel.publish(Twist())

        if success:
            result.result_data = [self.orientation_y]
            self.server.set_succeeded(result)


def main():
    rospy.init_node('circle_action_server')
    server = CircleActionServer()
    rospy.spin()


if _name_ == '_main_':
    main()
