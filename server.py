##############################################################################
# server.py
##############################################################################

import socket
import chatlib
import select
import random
# GLOBALS
users = {}#sort by score
questions = {}#ket: user name value: last quation
logged_users = {} # a dictionary of client hostnames to usernames 
messages_to_send = []# List of all messages that wait to send.

# CONSTANTS
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"#localhost
MAX_MSG_SIZE=1024#Max size in byte.

# HELPER SOCKET METHODS

def build_and_add_message(conn, code, msg):
	"""
	Builds a new message using chatlib, wanted code and message. 
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
	full_msg = chatlib.build_message(code,msg)
	messages_to_send.append((conn,full_msg))
	
	
	print("[SERVER] ",full_msg)	  # Debug print

def recv_message_and_parse(conn):
	"""
	Recieves a new message from given socket,
	then parses the message using chatlib.
	Paramaters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message. 
	If error occured, will return None, None
	"""
	full_msg = conn.recv(1024).decode()#recve a msg and decoed it.
	cmd, data = chatlib.parse_message(full_msg)#prosses the messege and return the comend and data.
	print("[CLIENT] ",full_msg)	  # Debug print
	return cmd, data
	
def create_random_question(username):
	"""
		Genarate random quation and orgnaize by the protocal, quation#answers#courrect quation
		Recives: user name
		Returns: random quation
	"""	

	All_questions = load_questions()
	questions_number = random.choice(list(All_questions.keys()))
	users[username]["questions_asked"].append(questions_number)
	questions=All_questions[questions_number]
	quation =str(questions_number)+"#"+ questions["question"]+"#"+ "#".join(questions["answers"])
	return quation

# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
	questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	
	return questions

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
	return users

	
# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	print("Setting up server... ")
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.bind((SERVER_IP,SERVER_PORT))
	sock.listen()
	return sock
	


		
def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	build_and_add_message(conn,chatlib.PROTOCOL_SERVER["error_message"],error_msg)
	print(error_msg)
	return None
	


	
##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
	"""
	Send user name score.
	Recieves: socket and user name
	Return: -
	"""
	global users
	score = users[username]["score"]
	build_and_add_message(conn,chatlib.PROTOCOL_SERVER["send_score"],str(score))


def handle_highscore_message(conn):
	"""
	send list of all user's scores

	"""
	global users
	All_scors = ""
	users=dict(sorted(users.items(), key=lambda item: item[1]['score']))#Soret all users by score.
	for user in users.keys():
		temp = str(users[user]["score"])
		All_scors += f"{user} : {temp}\n"
	build_and_add_message(conn,chatlib.PROTOCOL_SERVER["send_all_score"],All_scors)
	
def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
	global logged_users
	logged_users.pop(conn.getpeername(),None)
	conn.close()


def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  
	global logged_users	 
	msg_parts =list(data.split('#')) # split the messege into user name and password
	user_name = msg_parts[0]
	user_password = msg_parts[1]
	if user_name in users.keys():
		if user_password == users[user_name]['password']:
			logged_users[conn.getpeername()] = user_name
			build_and_add_message(conn,chatlib.PROTOCOL_SERVER["login_ok"],"")

		else:
			build_and_add_message(conn,chatlib.PROTOCOL_SERVER["login_failed_msg"],"wrong password")

	else:
		build_and_add_message(conn,chatlib.PROTOCOL_SERVER["login_failed_msg"],"wrong user name")


def handle_logged_message(conn):
	"""
		send all login users
	"""
	global logged_users
	login_users =",".join(list(logged_users.values()))
	build_and_add_message(conn,chatlib.PROTOCOL_SERVER["send_login_users"],login_users)


def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users	 
	print(logged_users)
	if conn.getpeername() in logged_users.keys():
		if cmd == "LOGOUT":
			handle_logout_message(conn)

		elif cmd == "LOGGED":
			handle_logged_message(conn)

		elif cmd == "MY_SCORE":
			handle_getscore_message(conn,logged_users[conn.getpeername()])
				
		elif cmd == "HIGHSCORE":
			handle_highscore_message(conn)
		elif cmd == "GET_QUESTION":
			handle_question_message(conn,logged_users[conn.getpeername()])
		elif cmd == "SEND_ANSWER":
			handle_answer_message(conn,logged_users[conn.getpeername()],data)
		else:
			build_and_add_message(conn,chatlib.PROTOCOL_SERVER["error_message"],f"unkonw comend,{cmd}")

	else:	
		if cmd == "LOGIN":# if user ask to login
			handle_login_message(conn,data)
		else:
			build_and_add_message(conn,chatlib.PROTOCOL_SERVER["error_message"],"wrong user name")
	
def handle_answer_message(conn,username,answer):
	"""
	Check user answer and send back result 
	Recieves: socket, user name and the user answer
	Return: - 
	"""
	
	l = list(answer.split("#"))
	quation_number = l[0]
	client_answer = l[1]
	courect_answer = load_questions()[int(quation_number)]["correct"]
	if client_answer == str(courect_answer):
		users[username]["score"]+=5
		build_and_add_message(conn,chatlib.PROTOCOL_SERVER["currect"],"")
		print("currect!")
	else:
		build_and_add_message(conn,chatlib.PROTOCOL_SERVER["wrong"],str(courect_answer))
		print("wrong!")



def handle_question_message(conn,username):
	"""
	Chose a quation and send it to the user
	Recieve: socket
	Return: -
	"""
	global questions
	questions[username] = create_random_question(username)
	print(questions)
	build_and_add_message(conn,chatlib.PROTOCOL_SERVER["send_quation"],questions[username])
	




	


def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global messages_to_send
	users = load_user_database()
	data = ""
	clinet_sockets = []
	print("Welcome to Trivia Server!")
	server_socket = setup_socket()

	cmd=""
	while True:
		try:
			ready_to_read,ready_to_write,in_error = select.select([server_socket]+clinet_sockets,[],[])
			for current_socket in ready_to_read:
				if current_socket == server_socket:
					(clinet_socket , clinet_address) = server_socket.accept()
					print("New client join", clinet_address)
					clinet_sockets.append(clinet_socket)
				else:
					print("New data")
					data = current_socket.recv(MAX_MSG_SIZE).decode()
					print("client send: ",data)
					cmd , msg = chatlib.parse_message(data)
					if len(clinet_sockets)==1 and cmd == "LOGOUT":
						break
					handle_client_message(current_socket,cmd,msg)
			for msg in messages_to_send:
				print("send")
				msg[0].send(msg[1].encode())
			messages_to_send=[]

		
		except Exception as e:
			print("main: "+str(e))
			(clinet_socket , clinet_address) = server_socket.accept()
		
		

		
	server_socket.close()





	



if __name__ == '__main__':
	main()

	