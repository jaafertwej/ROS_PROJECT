
import rospy
from geometry_msgs.msg import Pose, Point, Quaternion, Twist



class ARtag(object):

    def __init__(self, id, position, quaternion):
        self.id = id
        self.pose = Pose(position, quaternion);



        waypoints = list()

        for tag in tag_list:
        	waypoints.append( )# append tags pose from json file !!

        self.init_markers()

        for waypoint in waypoints:           
            p = Point()
            p = waypoint.position
			self.markers.points.append(p)

                    
    def init_markers(self,keyPoint):
        # Set up our waypoint markers
        marker_scale = 0.2
        marker_lifetime = 0 # 0 is forever
        marker_ns = 'waypoints'
        marker_id = keyPoint.id
        marker_color = {'r': 1.0, 'g': 0.7, 'b': 1.0, 'a': 1.0}
        
        # Define a marker publisher.
        self.marker_pub = rospy.Publisher('waypoint_markers', Marker, queue_size=5)
        
        # Initialize the marker points list.
        self.markers = Marker()
        self.markers.ns = marker_ns
        self.markers.id = marker_id
        self.markers.type = Marker.CUBE_LIST
        self.markers.action = Marker.ADD
        self.markers.lifetime = rospy.Duration(marker_lifetime)
        self.markers.scale.x = marker_scale
        self.markers.scale.y = marker_scale
        self.markers.color.r = marker_color['r']
        self.markers.color.g = marker_color['g']
        self.markers.color.b = marker_color['b']
        self.markers.color.a = marker_color['a']
        
        self.markers.header.frame_id = 'map'
        self.markers.header.stamp = rospy.Time.now()
		self.markers.points = list()
		p = Point(keyPoint.pose.position.x, keyPoint.pose.position.y, keyPoint.pose.position.z)
        self.waypoint_markers.points.append(p)

        # Publish the waypoint markers
        self.marker_pub = rospy.Publisher('waypoint_markers', Marker)

        self.marker_pub.publish(self.waypoint_markers)
