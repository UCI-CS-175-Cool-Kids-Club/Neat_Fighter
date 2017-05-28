from time import time
from numpy import trapz

INFLICTED_DAMAGE_SCALE = 2#40
TIME_SCALE = 0.01#1
DISTANCE_SCALE = 0.01#100

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

		print "Distance", self.distance_area
		return self.inflicted_damage * INFLICTED_DAMAGE_SCALE - (self.mission_time * TIME_SCALE) - DISTANCE_SCALE * self.distance_area

	def SetInflictedDamage(self, damage):
		self.inflicted_damage = damage

	def SetMissionTime(self, time):
		self.mission_time = time




