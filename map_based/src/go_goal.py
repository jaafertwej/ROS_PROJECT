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


class Localizing(State):

    def __init__(self):

        State.__init__(self, outcomes=['success', 'failed'])
        self.goNext = False

        print 'Start Localizing state'

    def execute(self, userdata):
        pub = rospy.Publisher(
            'initialpose', PoseWithCovarianceStamped)
        print 'Finding the initial point...'
        try:
            searchObject = SearchTags()
            # rospy.spin()
            while not rospy.is_shutdown():
                rospy.sleep(1)
                if searchObject.foundTag:
                    break
            print('success')
            print('jaafer123')
            self.goNext = searchObject.foundTag
        except rospy.ROSInterruptException:
            rospy.loginfo("AR Tag Tracker node terminated.")
        if self.goNext:
            try:
                print('asdasfkasdjfg')
                poseObject = TagsCOG()
                while not rospy.is_shutdown():
                    rospy.sleep(1)
                    self.robotPose = poseObject.getPose()
                    if self.robotPose is not None:
                        break
                # rospy.spin()
                
            except rospy.ROSInterruptException:
                rospy.loginfo("AR Tag Tracker node terminated.")

        # launch.shutdown()
        rospy.sleep(4)

        pose = PoseWithCovarianceStamped()
        pose.header.frame_id = "map"
        pose.pose.pose.position.x = self.robotPose.position.x
        pose.pose.pose.position.y = self.robotPose.position.y
        pose.pose.pose.position.z = self.robotPose.position.z
        pose.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]

        pose.pose.pose.orientation.x = 0
        pose.pose.pose.orientation.y = 0
        pose.pose.pose.orientation.z = self.robotPose.orientation.z
        pose.pose.pose.orientation.w = self.robotPose.orientation.y

        rospy.loginfo(pose)
        print(pose)
        rospy.sleep(1)
        
        while not rospy.is_shutdown():
            pub.publish(pose)
            print('jaafer5959598595959')
            rospy.sleep(1)
            

        success = True
        if success:
            rospy.loginfo("Robot is Localized")
            return 'success'
        else:
            return 'failed'


class Initializing(State):

    def __init__(self):

        State.__init__(self, outcomes=['success', 'failed'])

        # Initial pose
        self.position = {'x': 1.34, 'y': 2.15}
        self.quaternion = {'r1': 0.000, 'r2': 0.000, 'r3': -0.69, 'r4': 0.72}

        print 'Start Initializing...'

    def execute(self, userdata):

        navigator = GoToPose()

        print 'Moving To Initial pose'

        rospy.loginfo("Go to (%s, %s) pose",
                      self.position['x'], self.position['y'])

        success = navigator.goto(self.position, self.quaternion)

        if success:
            rospy.loginfo("Reached the Initial pose")
            return 'success'
        else:
            return 'failed'


class Loading(State):

    def __init__(self):

        State.__init__(self, outcomes=['success', 'failed'])

        # Loading area pose
        self.position = {'x': -0.71, 'y': 1.75}
        self.quaternion = {'r1': 0.000, 'r2': 0.000, 'r3': 1.00, 'r4': 0.00}

        print 'Start Moving to Loading area'

    def execute(self, userdata):

        navigator = GoToPose()

        print 'Moving To Loading area'

        rospy.loginfo("Go to (%s, %s) pose",
                      self.position['x'], self.position['y'])

        success = navigator.goto(self.position, self.quaternion)

        if success:
            rospy.loginfo("Reached the Loading area")
            print 'Loading...'
            # Wait for 10 seconds
            rospy.sleep(10.)
            return 'success'
        else:
            return 'failed'


class Unloading(State):

    def __init__(self):

        State.__init__(self, outcomes=['success', 'failed'])

        # Unloading area pose
        self.position = {'x': 2.29, 'y': 4.20}
        self.quaternion = {'r1': 0.000, 'r2': 0.000, 'r3': 0.00, 'r4': 1.00}

        print 'Start Moving to Unloading area'

    def execute(self, userdata):

        navigator = GoToPose()

        print 'Reached the Unloading area'

        rospy.loginfo("Go to (%s, %s) pose",
                      self.position['x'], self.position['y'])

        success = navigator.goto(self.position, self.quaternion)

        if success:
            rospy.loginfo("Reached the Unloading area")
            print 'Unloading...'
            # Wait for 10 seconds
            rospy.sleep(10.)
            return 'success'
        else:
            return 'failed'



if __name__ == '__main__':

    rospy.init_node('map_based', anonymous=False)

    StateGoal = StateMachine(outcomes=['success'])

    with StateGoal:

        StateMachine.add('Loading', Loading(), transitions={'success': 'Unloading', 'failed': 'Loading'})
        StateMachine.add('Unloading', Unloading(), transitions={'success': 'Loading', 'failed': 'Unloading'})

    StateGoal.execute()
