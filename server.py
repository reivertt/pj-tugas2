from socket import *
import socket
import threading
import logging
from datetime import datetime

HOST = '0.0.0.0'
PORT = 45000

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		try:
			while True:
				data = self.connection.recv(1024)
				if not data:
					break
				
				decoded = data.decode('utf-8').strip()
				logging.warning(f"Received from {self.address}: {decoded}")
				if decoded == "QUIT":
					logging.warning(f"Client {self.address} requested to quit")
					break
				elif decoded == "TIME":
					now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					response = f"JAM {now}\r\n"
					self.connection.sendall(response.encode('utf-8'))
				
		except Exception as e:
			logging.error(f"Error handling client {self.address}: {e}")
		finally:
			self.connection.close()
			logging.warning(f"Connection with {self.address} closed")
        

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind((HOST,PORT))
		self.my_socket.listen(1)
		logging.warning(f"Server listening on port {PORT}")
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()
