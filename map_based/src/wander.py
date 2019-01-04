#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from ar_track_alvar_msgs.msg import AlvarMarkers
import tf2_ros
import tf2_geometry_msgs
from python_json import PoseLoader
import numpy as np







class SearchTags():
    def __init__(self):
        self.g_range_ahead = 1 # anything to start
        self.scan_sub = rospy.Subscriber('scan', LaserScan, self.scan_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        # rospy.init_node('wander')
        self.state_change_time = rospy.Time.now()
        self.driving_forward = True
        self.rate = rospy.Rate(10)
        self.foundTag = False
        
        self.tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        self.choice = 0
        
        rospy.Subscriber("ar_pose_marker", AlvarMarkers, self.get_tags)
        rospy.loginfo("Publishing combined tag COG on topic /target_pose...")

    def scan_callback(self, msg):
        cleanedList = [x for x in msg.ranges if str(x) != 'nan']
        self.g_range_ahead = min(cleanedList)

    def getId(self, msg):
      ids = []
      for i in range(len(msg)):
        ids[i] = msg[i].id
      return ids


    def get_tags(self, msg):        
        # Get the number of markers
        tag_ids = [0, 1]
        n = len(msg.markers)
        myIdList = self.getId(msg.markers)
        print(msg.markers)
        # If no markers detected, just return
        if n == 0:
          self.foundTag = False
          self.move_to_tag()

        elif (tag_ids[self.choice] in myIdList):

          self.foundTag = True
          print('found Tag {}'.format(self.choice))
          # rospy.signal_shutdown('Quit1')
        else:
          self.foundTag = False
          self.move_to_tag()

    def setChoice(self, choice):
      self.choice = choice
          


    def move_to_tag(self):
          i = 0
          while not rospy.is_shutdown():
            i = i + 1
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


