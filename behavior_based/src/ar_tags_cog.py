#!/usr/bin/env python



import rospy
from tf import transformations, TransformerROS
from geometry_msgs.msg import Point, PoseStamped, Quaternion, Pose
from ar_track_alvar_msgs.msg import AlvarMarkers
import tf2_ros
import tf2_geometry_msgs
from python_json import PoseLoader
import numpy as np


class TagsCOG():
    def __init__(self):
        # rospy.init_node("ar_tags_cog")
        
        # Read in an optional list of valid tag ids
        self.tag_ids = rospy.get_param('~tag_ids', None)
        self.tf_buffer = tf2_ros.Buffer(rospy.Duration(1200.0)) #tf buffer length
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        
        # Publish the COG on the /target_pose topic as a PoseStamped message
        self.tag_pub = rospy.Publisher("target_pose", PoseStamped, queue_size=5)
        rospy.Subscriber("ar_pose_marker", AlvarMarkers, self.get_tags)
        
        rospy.loginfo("Publishing combined tag COG on topic /target_pose...")
        self.newPose = None
                
    def get_tags(self, msg):
        # Initialize the COG as a PoseStamped message
        tag_cog = PoseStamped()
        # Get the number of markers
        n = len(msg.markers)
        print('jaafer')
        
        # If no markers detected, just return
        if n == 0:
            return

        # Iterate through the tags and sum the x, y and z coordinates            
        for tag in msg.markers:
            
            # Skip any tags that are not in our list
            if self.tag_ids is not None and not tag.id in self.tag_ids:
                continue
            
            # Sum up the x, y and z position coordinates of all tags
            tag_cog.pose.position.x += tag.pose.pose.position.x
            tag_cog.pose.position.y += tag.pose.pose.position.y
            tag_cog.pose.position.z += tag.pose.pose.position.z

            tag_cog.pose.orientation.x += tag.pose.pose.orientation.x
            tag_cog.pose.orientation.y += tag.pose.pose.orientation.y
            tag_cog.pose.orientation.z += tag.pose.pose.orientation.z
            tag_cog.pose.orientation.w += tag.pose.pose.orientation.w

            
             # Compute the COG
            tag_cog.pose.position.x /= n
            tag_cog.pose.position.y /= n
            tag_cog.pose.position.z /= n
            
            # Give the tag a unit orientation
            # tag_cog.pose.orientation.w = 1

            # Add a time stamp and frame_id
            tag_cog.header.stamp = rospy.Time.now()
            tag_cog.header.frame_id = msg.markers[0].header.frame_id

            # Publish the COG
            self.tag_pub.publish(tag_cog)

            myTagList = self.getTagsList()
            myTag = myTagList[tag.id]
            self.newPose = self.estimateNewPose(myTag, tag_cog.pose)
            print(self.newPose)
            # rospy.signal_shutdown('Quit2')
            


    def getPose(self):
      newPose = self.newPose
      return newPose

    def getTagsList(self):
        loader = PoseLoader("./pose_dict.json")
        poses = loader.geometry_pose()
        return poses


    def estimateNewPose(self, tagPoseGlobal, turPoseLocal):
        
        T1 = self.getTransformationMatrix(turPoseLocal)
        T2 = self.getTransformationMatrix(tagPoseGlobal)
        T3 = T2 * T1


        position = Point(T3[0,3], T3[1,3], 0)
        orientation = self.getQFromRotation(T3[:3, :3])
        newPose = Pose(position, orientation)
        return newPose

    def getTransformationMatrix(self, pose):

        [roll, pitch, yaw] = transformations.euler_from_quaternion(np.squeeze(np.array([[pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w]])))
        
        t = np.array([[pose.position.x, pose.position.y, pose.position.z, 1]])
        Rx = np.matrix([[1,           0,          0],
                       [0, np.cos((roll)), -np.sin((roll))],
                       [0, np.sin((roll)), np.cos((roll))]])

        Ry = np.matrix([[np.cos((pitch)) , 0, np.sin((pitch))],
                       [0,           1,          0],
                       [-np.sin((yaw)), 0, np.cos((pitch))]])

        Rz = np.matrix([[np.cos((yaw)) ,-np.sin((yaw)) ,0],
                       [np.sin((yaw)) , np.cos((yaw)), 0],
                       [0,           0,          1]])
        R = Rz * Ry * Rx
        R = np.vstack((R, [0,           0,          0]))
        T = np.hstack((R, t.T))
        return T

    def getQFromRotation(self, R):

        qw = np.sqrt(1+R[0,0] + R[1,1]+ R[2,2])/2
        qx = (R[2,1] - R[1,2])/(4*qw)
        qy = (R[0,2] - R[2,0])/(4*qw)
        qz = (R[1,0] - R[0,1])/(4*qw)

        return Quaternion(qx, qy, qz, qw)
  
if __name__ == '__main__':
    try:
        TagsCOG()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AR Tag Tracker node terminated.")
