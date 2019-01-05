import json
from geometry_msgs.msg import Pose , Point ,Quaternion


class PoseLoader(object):
	"""docstring for PoseLoader"""
	def __init__(self,file_path):

		self.path = file_path

	def read_pose(self):
		with open(self.path) as f:
			self.data = json.load(f)

	def geometry_pose(self):
		self.read_pose()
		Poses = []
		for i in range(len(self.data)):
			tag_id = self.data[i]["Id"]
			pos = self.data[i]["position"]
			ori = self.data[i]["orientation"]
			Poses.append(Pose(Point(pos['x'], pos['y'],pos['z']),Quaternion(ori['x'],ori['y'],ori['z'],ori['w'])))
		return Poses
