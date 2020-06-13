from cheese_stack import CheeseStack
from cheese import Cheese, ReblochonCheese

from socket import socket, create_connection, gethostname, gethostbyname_ex

from threading import Thread, Timer
import threading

import json
import pickle
import os
import time

TRACKER_IP = "192.168.0.38"
TRACKER_PORT = 20000 

MY_IP = "192.168.0.38"

class Member:
	
	CHAIN_PATH = str(os.path.expanduser("~")) + "/.cheese_stack/"
	os.makedirs(CHAIN_PATH, exist_ok=True)


	def myReadLine(self, connection): #It is a function to read in a connection.
		readval = b""
		flag = True
		while flag:
			byte = connection.recv(1)
			if byte == b"\n":
				flag = False
			else:
				readval += byte
		return readval

	def __init__(self, member_id, port=1114): 
		self.id = member_id  #Identification of the member.
		self.path = Member.CHAIN_PATH + str(port)
		self.port = port
		self.memberList = []
		self.registered = False
		self.cheesestack = self.reloadCheeses()
		self.longest_valid_cheesestack = self.reloadCheeses()

	def activateMember(self): #In this function we activate the member to start sniffing the cheese and dumping the cheese
		def loop():
			self.register()
			while True: 
				Thread(target=self.dumpCheese).start()
				Thread(target=self.sniffCheeses).start()
				time.sleep(10 ) #Takes 10 seconds to sniff
		Thread(target=loop).start()

	def reloadCheeses(self):#Reload the pre-existing cheese
		try:
			return pickle.load(open(self.path, "rb"))
		except:
			return CheeseStack()

	def dumpCheese(self):        
		pickle.dump(self.cheesestack, open(self.path, "wb")) #Save the pre-existing cheese

	def updateLongestCheeseStack(self):
		if self.cheesestack.isValid() and len(self.cheesestack.stack) > len(self.longest_valid_cheesestack.stack):
			self.longest_valid_cheesestack = self.cheesestack
                #(for newly mined cheese) if the cheesestack is valid and if the length of the cheesestack is greater than the longest cheesestack then update the longest cheesestack 
		received_cheese_stack = self.fetchCheeseStack()
		#(Sniffing around: Taking the cheesestack from other members) same condition as before
		if received_cheese_stack.isValid() and len(received_cheese_stack.stack) > len(self.longest_valid_cheesestack.stack):
                    
			self.longest_valid_cheesestack = received_cheese_stack
			#Update the longest cheesestack

	def fetchCheeseStack(self):
		new_cheese_stack = self.cheesestack
		self.fetchMembers()    
		for mem  in self.memberList:#goes into the member list
			ip = mem["member_ip"]#all the IP address of the members
			port = mem["member_port"]#all the ports of the members
			try:
				connection = create_connection((ip, port))
				connection.sendall(b"GETCHEESESTACK\n")
				print("Member ", self.id, " transmitted the request for cheesestack")
				self.memberList = []
				response = self.myReadLine(connection).decode("utf-8")
				connection.close()
				if response == "NONE":
					print(self.id, " got nothing")
					continue
				else:
					cs = pickle.loads(response)
					if len(cs.stack) > len(new_cheese_stack.stack):
						new_cheese_stack = cs

			except Exception as e:
				print("Member ", self.id, " Error in getting CheeseStack: ", e)

		return new_cheese_stack #Returns the longest cheesestack from the neighbours

	def register(self): #registering with the tracker
		try:
			connection = create_connection((TRACKER_IP, TRACKER_PORT))
			connection.sendall(b'REGISTER\n') # TODO: send network ip?
			connection.sendall(bytes(str(self.port) + '\n', 'utf-8')) 
			connection.close()
			self.registered = True
		except Exception as e:
			print("Error in registering the Member: ", self.id, " ", e)

	def fetchMembers(self): #calls tracker to get the member list
		try:
			connection = create_connection((TRACKER_IP, TRACKER_PORT))
			connection.sendall(b"GETMEMBERS\n")
			print("Member ", self.id, " transmitted the request for Member List")
			self.memberList = []
			while True:
				l = self.myReadLine(connection).decode("utf-8")
				if l == "200":
					break
				else:
					print("Member ", self.id, " got the Member List in JSON: ", l)
					self.memberList = json.loads(l)

		except Exception as e:
			print("Error in getting the Members by : ", self.id, " ", e)

	def startListening(self):
		listenerSocket = socket() #Binding to a socket
		listenerSocket.bind((MY_IP, self.port))
		listenerSocket.listen() #Listening on the port
		print("Member ", self.id, " is listening on port: ", self.port ) #With a port number
		def listenerThread(): #we call all the bytes function
			while True:
				connection, addr = listenerSocket.accept()
				print("Handling the connection by Member: ", self.id, " on Address: ", addr)
				Thread(target=self.handleClient, args=(connection,)).start()
                                #we call the handleClient function if we have new bytes
		Thread(target=listenerThread).start()

	def sendTransactionDetails(self, connection):
		seq_num = self.myReadLine(connection).decode("utf-8")
		seq_num = int(seq_num)
		print("Member ", self.id, " received the request for Transaction details with sequence number: ", seq_num)

		chsedump = pickle.dumps(self.cheesestack.stack[seq_num].content)#look at the sequence number requested
		connection.sendall(chsedump)
		connection.sendall(b"\n")
		print("Member ", self.id, " transmitted the transaction details: ", self.cheesestack.stack[seq_num].content)
                #sends the cheese of that sequence number
	def sendCheese(self, connection): 
		seq_num = self.myReadLine(connection).decode("utf-8")
		seq_num = int(seq_num) 
		print("Member ", self.id, " received the request for cheese with sequence number: ", seq_num)
		if len(self.cheesestack.stack) > seq_num:
			chsedump = pickle.dumps(self.cheesestack.stack[seq_num])
			connection.sendall(chsedump)
			connection.sendall(b"\n")
			print("Member ", self.id, " transmitted the cheese: ", self.cheesestack.stack[seq_num])
		else:
			connection.sendall(b"NONE\n")
			print("Member ", self.id, " got invalid Cheese request")

	def getCheese(self, connection): #get the cheese and check its validity
		chsedump = self.myReadLine(connection).decode("utf-8")
		chse = pickle.loads(chsedump) 
		print("Member ", self.id, " received the cheese: ", chse)
		if len(self.cheesestack.stack) != chse.seq_num:
			print("Member ", self.id, " dropped the cheese")
			connection.sendall(b"DROP\n")
		else:    
			status = self.cheesestack.insertCheese(chse)#Also updates the longest cheese
			self.updateLongestCheeseStack()
			if status:
				print("Member ", self.id, " inserted the received cheese")
				connection.sendall(b"OK\n")
				self.broadcastCheese(chse.seq_num)
			else:
				print("Member ", self.id, " got the invalid cheese")
			 	connection.sendall(b"INVALID\n")

	def getTransaction(self, connection): 
		txndump = self.myReadLine(connection).decode("utf-8")
		txn = pickle.loads(txndump)
		connection.sendall(b"200\n")
		print("Member ", self.id, " received the transaction: ", txn)
		if self.cheesestack.checkBalance(txn) is True:
                        #We only care about the transactions feasible
			self.cheesestack.createCheese(txn)#create a new cheese with transaction
			self.broadcastCheese(len(self.cheesestack.stack)-1)#broadcasts the cheese

	def sendCheeseStack(self, connection):#gets the whole cheese stack and transmits it to the one who asked
		chsestackdump = pickle.dumps(self.cheesestack)
		connection.sendall(chsestackdump)
		connection.sendall(b"\n")
		print("Member ", self.id, " did transmit the CheeseStack: ", self.cheesestack)

	def responseToPing(self, connection):
		print("Member ", self.id, " received the ping request")
		connection.sendall(b"200\n")
		print("Member ", self.id, " responsed to ping")

	def handleClient(self, connection): 
		l = self.myReadLine(connection).decode("utf-8")

		if l == "PING": #sends 200 if it receives a ping
			self.responseToPing(connection)
		
		if l == "SENDCheese": #If a member sends a cheese, it calls the SENDCheese function 
			self.getCheese(connection)

		if l == "SENDTrnxn":
			self.getTransaction(connection)
		
		if l == "GETCheese":
			self.sendCheese(connection)

		if l == "GETCHEESESTACK":
			self.sendCheeseStack(connection)

		if l == "GETRXN":
			self.sendTransactionDetails(connection)

		connection.close()

	def getSniffedCheese(self, connection):#looks for all the cheese that has been transmitted
		response = self.myReadLine(connection).decode("utf-8")
		connection.close()
		status_sniff = False
		if response == "NONE":
			print("Member ", self.id, " did not receive the cheese that it requested")
			return status_sniff
		else:
			chse = pickle.loads(response)
			print("Member ", self.id, " received the cheese: ", chse)
                        #if received calls the insert cheese function to check validity
			status = self.cheesestack.insertCheese(chse)
			self.updateLongestCheeseStack()
			#either results in adding that cheese or ignoring that cheese
			if status:
				print("Member ", self.id, " Added a new cheese")
			else:
				print("Member ", self.id, " Ignored the cheese")
			status_sniff = True
			return status_sniff

	def sniffCheeses(self):
		self.fetchMembers()    
		for mem in self.memberList:
			ip = mem["member_ip"]
			port = mem["member_port"]
			fetchseq = str(len(self.cheesestack.stack))
			try:
				connection = create_connection((ip, port))
				connection.sendall(b'GETCheese\n')
				print("Member ", self.id, " sent the cheese request")
				connection.sendall(bytes(fetchseq + '\n', 'utf-8'))
				print("Member ", self.id, " transmitted the cheese request for sequence number: ", fetchseq)
				if not self.getSniffedCheese(connection):
					continue

			except Exception as e:
				print("sniffing error: ", e)

	def broadcastCheese(self, seq_num):
		def broadcastThread(): #everytime it gets a new cheese, it will broadcast it to all the members in the members list
			self.fetchMembers()
			chsedump = pickle.dumps(self.cheesestack.stack[seq_num])
			for mem in self.memberList:
				ip = mem["member_ip"]
				port = mem["member_port"]
				try:
					connection = create_connection((ip, port))
					connection.sendall(b'SENDCheese\n')
					print("Member ", self.id, " broadcasted the cheese")
					connection.sendall(chsedump)
					connection.sendall(b"\n")
					print("Transmitted Cheese:", self.cheesestack.stack[seq_num])
					response = self.myReadLine(connection).decode("utf-8")
					print("Member ", self.id, " received the broadcast response: ", response)
					connection.close()
					self.registered = True
				except Exception as e:
					print("Member ", self.id, " had the broadcast error: ", e)

		Thread(target=broadcastThread).start()

	def shareTransactionDetails(self, transaction):
		#def transactionBroadcast():
		self.fetchMembers()
		trxndump = pickle.dumps(transaction) #broadcasts the transaction to the whole member list
		for mem in self.memberList:
			ip = mem["member_ip"]
			port = mem["member_port"]
			if port!=str(self.port):
				try:
					connection = create_connection((ip, port))
					connection.sendall(b'SENDTrnxn\n')
					print("Member ", self.id, " broadcasted the Transaction")
					connection.sendall(trxndump)
					connection.sendall(b"\n")
					print("Transmitted transaction:", transaction)
					response = self.myReadLine(connection).decode("utf-8")
					print("Member ", self.id, " received the broadcast transaction response: ", response)
					connection.close()

				except Exception as e:
					print("Member ", self.id, " had the broadcast error: ", e)

		#Thread(target=transactionBroadcast).start()

	def requestTransactionDetails(self, seq_num):#one member request transaction details of another
		#def transactionRequestBroadcast():
		self.fetchMembers()
		trnxn = ""
		for mem in self.memberList:
			ip = mem["member_ip"]
			port = mem["member_port"]
			if port!=str(self.port):
				try:
					connection = create_connection((ip, port))
					connection.sendall(b"GETRXN\n")
					connection.sendall(bytes(str(seq_num) + '\n', 'utf-8'))#look for the sequence number
					#connection.sendall(b"\n")
					print("Member ", self.id, " transmitted the request for transaction details")
					response = self.myReadLine(connection).decode("utf-8")
					connection.close()
					if response == "NONE":
						print(self.id, " got nothing")
						continue
					else:
						trnxn = pickle.loads(response)
						break

				except Exception as e:
					print("Member ", self.id, " Error in getting Transaction details: ", e) 

		return trnxn

		#Thread(target=transactionRequestBroadcast).start()
