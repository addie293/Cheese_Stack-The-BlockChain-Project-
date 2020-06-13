from socket import *
from threading import Thread

import json
import random
import time

tracker_ip = '192.168.137.1'
tracker_port = 20000

class Tracker:

	def __init__(self):
		self.membersList = []

	#Read in function... it takes a socket connection
	def myReadLine(self, connection):
		readval = b""  # gets an empty byte
		flag = True
		while flag:
			# here we check byte by byte
			byte = connection.recv(1)
			# until it gets a backslash n (gets a new line)
			if byte == b"\n":
				flag = False
			else:
				# otherwise add byte
				readval += byte
		# and we return the values
		return readval


	def startListning(self):
		def acceptAll():
			# we declare a socket
			serverSocket = socket()
			# this binds the ip and the port to the socket server
			serverSocket.bind((tracker_ip,tracker_port))
			# it starts listening and capturing bytes on it
			serverSocket.listen()
			while True:
				# for infinite loop we we accept all the bytes coming from any client
				conn, addr = serverSocket.accept()
				# we call the handleClient function with the connection  and the ip as paramters
				self.handleClient(conn, addr[0])
		
		def pingAll():

			# in an infinite loop we ping all the members
			while True:
				print("Pinging all members")

				# we loop throurgh the members list and we get the ip and the port
				for mem in self.membersList:
					# we check if we there is any live member
					try:
						ip = mem["member_ip"]
						port = mem["member_port"]
						print("Starting ping member:",ip,port)
						conn = create_connection((ip,port))
						conn.sendall(b"PING\n") # we send the PING string to the members
						l = self.myReadLine(conn).decode("utf-8")
						# we check if they are live (if we get the reply 200 it means the are live)
						if l != "200":
							print("Pinging the Member:",ip,port," with response: ",l)

						else:
							print("Pinging the Member:",ip,port," with response: ",l)
					except:
						print("Pinging the Member:",ip,port," Member timeout, Now deleting the Member!")
						# if the member is not live we delete the member
						self.membersList.remove(mem)
				time.sleep(60)


		# we start the Thread (Thread module is used to manage easly the execution of multiple threads)
		Thread(target=pingAll).start()
		Thread(target=acceptAll).start()
	
	# we call this function when we receive something
	def handleClient(self,conn, ip):
		def handle():
			
			l = self.myReadLine(conn).decode("utf-8")
			#print(l)
			#if it is REGISTER we get the port and the adress and we save it in a dictionary
			if l == "REGISTER":
				port = self.myReadLine(conn).decode("utf-8")
				addr = {}
				addr["member_ip"]= ip
				addr["member_port"] = port
				if addr not in self.membersList:
					self.membersList.append(addr) # we append that dictionary to a list
					print("Successfully adding the member: ",addr)
				# if it successfully registered we send 201
				conn.sendall(b"201\n")
			# if the call is to GETMEMBERS we convert the output to json
			elif l == "GETMEMBERS":
				conn.sendall((json.dumps(self.membersList)+"\n").encode('UTF-8'))
				# if it is true (we can get members) we send 200
				conn.sendall(b"200\n")
			else:
				conn.sendall(("FAIL"+"\n").encode('UTF-8'))
			conn.close()
		Thread(target=handle).start()


if __name__ == "__main__":
	t = Tracker()
	t.startListning()
