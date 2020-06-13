from cheese import Cheese, ReblochonCheese

class CheeseStack:
	Reblochon_Cheese = ReblochonCheese()

	def __init__(self):
		self.stack = [CheeseStack.Reblochon_Cheese]
	
	def createCheese(self, content):
		lastseq = self.stack[-1].seq_num # Sequence number of the last element of the stack


		# Check for the essence of Reblochon cheese that does not have a parent essence
		if self.stack[-1].seq_num!=0:
			lastessence = self.stack[-1].essence
		else:
			lastessence = self.stack[-1].parent_essence # Essence of normal cheese

		cheese = Cheese(content, lastseq + 1, lastessence)
		if self.insertCheese(cheese):
			return cheese
		else:
			return -1

	def insertCheese(self, cheese):
		# Recalculate the essence & check with the essence of the cheese for validity
		if cheese.essence != cheese.calculateEssence():
			return False
		# Hash has to pass the integer difficulty(0000-> 32 bytes)
		if not cheese.essence.startswith("0" * Cheese.DIFFICULTY):
			return False
		# Check sequence number of new cheese with the parent cheese
		if cheese.seq_num != self.stack[-1].seq_num + 1:
			return False
		# Check for parent cheese and normal cheese
		if self.stack[-1].seq_num!=0:
			if cheese.parent_essence != self.stack[-1].essence:
				return False
		else:
			if cheese.parent_essence != self.stack[-1].parent_essence:
				return False
		self.stack.append(cheese)
		return True

	def getCheeseBySeqNum(self, seq_num):
		return self.stack[seq_num]

	def dropLastCheese(self):
		self.stack.pop()

	def isValid(self):
		parent_essence = CheeseStack.Reblochon_Cheese.parent_essence #Check if it's the parent essence
		last_seq_num = 0	
		for cheese in self.stack[1:]:
			if cheese.essence != cheese.calculateEssence():
				return False
			if cheese.parent_essence != parent_essence:
				return False
			if not cheese.essence.startswith("0" * Cheese.DIFFICULTY):
				return False
			if cheese.seq_num != last_seq_num+1:
				return False
			parent_essence = cheese.essence
			last_seq_num = cheese.seq_num
		return True

	def checkBalance(self, content_received):
		client = content_received.split('_')[0]
		amount = int(content_received.split('_')[2])
		clientBalance = 0
		for b in self.stack[1:]:
			#transfer to the client
			if b.content.split('_')[1] == client:
				clientBalance = clientBalance + int(b.content.split('_')[2])
			#transfer from the client
			if b.content.split('_')[0] == client:
				clientBalance = clientBalance - int(b.content.split('_')[2])

		return amount <= clientBalance

	def __repr__(self):
		rp = "{CheeseStack"
		for b in self.stack:
			rp += " " + str(b)
		return rp + "}"

if __name__ == "__main__":
	c = CheeseStack()
	print(c.createCheese("A_B_500"))# A sends $500 to B
	print(c.createCheese("B_C_100"))# B sends $500 to c
	print(c.createCheese("C_A_101"))# C sends $500 to A

	print(c.checkBalance("A_B_100"))# Check if A has enough balance to send to B

	print(c)
	c.dropLastCheese()
	print(c)
	print(c.isValid())
