#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from ar_track_alvar_msgs.msg import AlvarMarkers
import tf2_ros
import tf2_geometry_msgs
from python_json import PoseLoader
import numpy as np



# def search():
#   rospy.Subscriber("ar_pose_marker", AlvarMarkers, get_tags)
    


# def get_tags(msg):

#   g_range_ahead = 1 # anything to start
#   scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)
#   cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
#   rospy.init_node('wander')
#   state_change_time = rospy.Time.now()
#   driving_forward = True
#   rate = rospy.Rate(10)
  
#   # Initialize the COG as a PoseStamped message
#   tag_cog = PoseStamped()
        
#     # Get the number of markers
#   n = len(msg.markers)
#   print('n is :{}'.format(n))
        
#   # If no markers detected, just return
#   if n == 0:
#     while not rospy.is_shutdown():
#       if driving_forward:
#         # BEGIN FORWARD
#         if (g_range_ahead < .8 or rospy.Time.now() > state_change_time):
#           driving_forward = False
#           state_change_time = rospy.Time.now() + rospy.Duration(5)

#         print("END FORWARD")
#       else: # we're not driving_forward
#         # BEGIN TURNING
#         if rospy.Time.now() > state_change_time:
#           driving_forward = True # we're done spinning, time to go forwards!
#           state_change_time = rospy.Time.now() + rospy.Duration(30)
#         # END TURNING
#       twist = Twist()

#       if driving_forward:
#         twist.linear.x = .3
#       else:
#         twist.angular.z = 1
#       cmd_vel_pub.publish(twist)
#       print('jaafer')
#       rate.sleep()






class SearchTags():
    def __init__(self):
        self.g_range_ahead = 1 # anything to start
        self.scan_sub = rospy.Subscriber('scan', LaserScan, self.scan_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        # rospy.init_node('wander')
        self.state_change_time = rospy.Time.now()
        self.driving_forward = True
        self.rate = rospy.Rate(10)
        print('jaafer')
        self.foundTag = False
        
        self.tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        
        rospy.Subscriber("ar_pose_marker", AlvarMarkers, self.get_tags)
        rospy.loginfo("Publishing combined tag COG on topic /target_pose...")

    def scan_callback(self, msg):
        cleanedList = [x for x in msg.ranges if str(x) != 'nan']
        self.g_range_ahead = min(cleanedList)
        print(self.g_range_ahead)
                
    def get_tags(self, msg):        
        # Get the number of markers
        n = len(msg.markers)
        print(n)
        # If no markers detected, just return
        if n == 0:
          self.foundTag = False
          i = 0
          while not rospy.is_shutdown():
            i = i + 1
            print(i)
            if i > 10:
              break
            if self.driving_forward:
              # BEGIN FORWARD
              if (self.g_range_ahead < .8 or rospy.Time.now() > self.state_change_time):
                self.driving_forward = False
                self.state_change_time = rospy.Time.now() + rospy.Duration(5)

            else: # we're not driving_forward
              # BEGIN TURNING
              if rospy.Time.now() > self.state_change_time:
                self.driving_forward = True # we're done spinning, time to go forwards!
                self.state_change_time = rospy.Time.now() + rospy.Duration(30)
              # END TURNING
            twist = Twist()

            if self.driving_forward:
              twist.linear.x = .3
            else:
              twist.angular.z = .5
            self.cmd_vel_pub.publish(twist)
            self.rate.sleep()
        else:
          self.foundTag = True
          print('found Tag')
          rospy.signal_shutdown('Quit')
          return


  
if __name__ == '__main__':
    try:
        searchObject = SearchTags()
        print(searchObject.foundTag)
        rospy.spin()
        print('success')
        print(searchObject.foundTag)


    except rospy.ROSInterruptException:
        rospy.loginfo("AR Tag Tracker node terminated.")