from time import time
from numpy import trapz

class AgentResult:
	def __init__(self):
		self.last_time = time()
		self.distance_area = 0.0


	def AppendDistance(distance):
		cur_time = time()
		time_dif = self.last_time - cur_time
		self.distance_area += time_dif * distance
		self.last_time = cur_time()

	def GetFitness(self):
		return 0




