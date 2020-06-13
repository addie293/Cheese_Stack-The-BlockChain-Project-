import hashlib
import random

class Cheese:

	DIFFICULTY = 4

	def __init__(self, content, seq_num, parent_essence):
		self.content = content
		self.seq_num = seq_num
		self.parent_essence = parent_essence
		self.updateEssence()
	
	def updateEssence(self):
		self.nonce = 0
		self.essence = ""
		while not self.essence.startswith("0" * Cheese.DIFFICULTY):
			self.nonce += random.randint(1,1000)
			self.essence = self.calculateEssence()

	def calculateEssence(self):
		encodedCheese = (
				str(self.content) +
				str(self.seq_num) +
				str(self.nonce) + 
				self.parent_essence).encode('utf-8')
		return hashlib.sha1(encodedCheese).hexdigest()

	def __repr__(self):
		return "<cheese " + str(self.seq_num) + " " + self.content + ">"

class ReblochonCheese:

	def __init__(self):
		self.content = "Öriginal_Cheese_0"
		self.seq_num = 0
		self.parent_essence = ""

	def __repr__(self):
		return "<cheese " + str(self.seq_num) + " " + self.content + ">"	

if __name__ == "__main__":
	c = Cheese("X_Y_1000", 123, "011")
	rc = ReblochonCheese()
	print(c)
	print(rc)
