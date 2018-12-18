import json
from geometry_msgs.msg import Pose , Point ,Quaternion

# a = {}
# a["Id"] = 0
# a["position"] = {"x":0.0 , "y":0.0 , "z":0.0}
# a["orientation"] = {"r1":0.0 , "r2":0.0 , "r3":0.0,"r4":0.0}




# r = json.dumps(a)
# loaded_r = json.loads(r)



# f = open("pose_dict.json","w")
# f.write(r)




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
			Poses.append(Pose(Point(pos['x'], pos['y'],pos['z']),Quaternion(ori['r1'],ori['r2'],ori['r3'],ori['r4'])))
		return Poses


loader = PoseLoader("./pose_dict.json")
poses = loader.geometry_pose()
print(poses[1].position)