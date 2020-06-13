from member import Member
from random import randint

import time


if __name__ == "__main__":

	member_list = [] # Create a member list

	start = time.time()

	for i in range(2): # Create a number of members with member id
		member_list.append(Member(i+1, randint(1000, 8999)))
		member_list[i].activateMember()# Activate the member
		member_list[i].startListening()# Member listen to a particular port

	# For all the members initiate a new transaction
	member_list[1].shareTransactionDetails("A_B_500") 
	#member_list[1].shareTransactionDetails("B_C_100")
	#member_list[0].shareTransactionDetails("C_A_101")
	#member_list[0].shareTransactionDetails("A_B_500")

        #It will take sometime(arbitrary)to validate the transaction to get
        #a stable cheese stack aka to make it harder to make change in the stack
	
	#while True:

		#if (time.time()-start > 10):
                        # Current cheese stack of members
			#print(member_list[0].cheesestack)
			#print(member_list[1].cheesestack)
			#print(member_list[0].requestTransactionDetails(1))
			#break
