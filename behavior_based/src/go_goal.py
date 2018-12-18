# TurtleBot must have minimal.launch & amcl_demo.launch
# running prior to starting this script
# For simulation: launch gazebo world & amcl_demo prior to run this script
#!/usr/bin/env python

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, PoseWithCovarianceStamped
from smach import State, StateMachine
import numpy as np
from geometry_msgs.msg import Twist
from GoToPose import GoToPose
from ar_tags_cog import TagsCOG
from wander import SearchTags
import roslaunch


# class Initializing(State):

#     def __init__(self):

#         State.__init__(self, outcomes=['success', 'failed'])
#         self.choice = 0
#         print 'Start Initializing...'

#     def execute(self, userdata):


#         print 'Finding the initial point...'
#         try:
#             searchObject = SearchTags()
#             searchObject.setChoice(self.choice)
#             while not rospy.is_shutdown():
#                 print(searchObject.foundTag)
#                 rospy.sleep(1)
#                 if searchObject.foundTag:
#                     break

#             # Run the Follower
#         except rospy.ROSInterruptException:
#             rospy.loginfo("AR Tag Tracker node terminated.")
            

#         success = True
#         if success:
#             rospy.loginfo("Robot is Localized")
#             return 'success'
#         else:
#             return 'failed'


class Loading(State):

    def __init__(self):

        State.__init__(self, outcomes=['success', 'failed'])
        self.choice = 0
        print 'Start Moving to Loading area'

    def execute(self, userdata):

        print 'Finding the initial point...'
        try:
            searchObject = SearchTags()
            searchObject.setChoice(self.choice)
            while not rospy.is_shutdown():
                rospy.sleep(1)
                if searchObject.foundTag:
                    break

            # Run the Follower
        except rospy.ROSInterruptException:
            rospy.loginfo("AR Tag Tracker node terminated.")
            

        success = True
        if success:
            rospy.loginfo("Robot is Localized")
            return 'success'
        else:
            return 'failed'



class Unloading(State):

    def __init__(self):

        State.__init__(self, outcomes=['success', 'failed'])
        self.choice = 1
        print 'Start Moving to Unloading area'

    def execute(self, userdata):


        print 'Finding the initial point...'
        try:
            searchObject = SearchTags()
            searchObject.setChoice(self.choice)
            while not rospy.is_shutdown():
                rospy.sleep(1)
                if searchObject.foundTag:
                    break

            # Run the Follower
        except rospy.ROSInterruptException:
            rospy.loginfo("AR Tag Tracker node terminated.")
            

        success = True
        if success:
            rospy.loginfo("Robot is Localized")
            return 'success'
        else:
            return 'failed'



if __name__ == '__main__':

    rospy.init_node('nav_test', anonymous=False)

    StateGoal = StateMachine(outcomes=['success'])

    with StateGoal:

        StateMachine.add('Loading', Loading(), transitions={'success': 'Unloading', 'failed': 'Loading'})
        StateMachine.add('Unloading', Unloading(), transitions={'success': 'Loading', 'failed': 'Unloading'})

    StateGoal.execute()
