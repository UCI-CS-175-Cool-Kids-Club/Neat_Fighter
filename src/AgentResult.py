from time import time

INFLICTED_DAMAGE_SCALE = 1000#40
TIME_SCALE = 20#1
DISTANCE_SCALE = 300#100

class AgentResult:
	def __init__(self):
		self.last_time = time()
		self.distance_area = 0.0
		self.inflicted_damage = 0
		self.mission_time = 0

	def AppendDistance(self,distance):
		cur_time = time()
		time_dif = cur_time - self.last_time
		self.distance_area += time_dif * distance
		self.last_time = cur_time

	def GetFitness(self):
		return self.inflicted_damage * INFLICTED_DAMAGE_SCALE - (self.mission_time * TIME_SCALE) - (self.distance_area * DISTANCE_SCALE)

	def SetInflictedDamage(self, damage):
		self.inflicted_damage = damage

	def SetMissionTime(self, time):
		self.mission_time = time




