#!/usr/bin/env python
import rospy
import actionlib
from actions_test.msg import VectorFeedback, VectorResult, VectorAction

class SequentialNumbersClass(object):
    
    # create messages that are used to publish feedback/result
    _feedback = VectorFeedback()
    _result = VectorResult()

    def __init__(self):
        # creates the action server
        self._as = actionlib.SimpleActionServer("vector_as", VectorAction, self.goal_callback, False)
        self._as.start()
    
    def goal_callback(self, goal):
        # this callback is called when the action server is called.
        # this is the function that computes the sequence of numbers
        # less than the goal.order and returns the sequence to the node that called the action server
    
        # helper variables
        r = rospy.Rate(1)
        success = True
    
        # initialize the sequence
        self._feedback.sequence = []

        # publish info to the console for the user
        rospy.loginfo('"vector_as": Executing, creating sequence of numbers less than %i' % goal.order)
    
        # starts calculating the sequence of numbers
        for i in range(goal.order):
    
            # check that preempt (cancellation) has not been requested by the action client
            if self._as.is_preempt_requested():
                rospy.loginfo('The goal has been cancelled/preempted')
                # the following line, sets the client in preempted state (goal cancelled)
                self._as.set_preempted()
                success = False
                # we end the calculation of the sequence
                break
      
            # append the current number to the feedback sequence
            self._feedback.sequence.append(i)
            # publish the feedback
            self._as.publish_feedback(self._feedback)
            # the sequence is computed at 1 Hz frequency
            r.sleep()
    
        # at this point, either the goal has been achieved (success==true)
        # or the client preempted the goal (success==false)
        # If success, then we publish the final result
        # If not success, we do not publish anything in the result
        if success:
            self._result.sequence = self._feedback.sequence
            rospy.loginfo('Succeeded creating the sequence of numbers less than %i' % goal.order)
            self._as.set_succeeded(self._result)
      
if __name__ == '__main__':
    rospy.init_node('sequential_numbers')
    SequentialNumbersClass()
    rospy.spin()

