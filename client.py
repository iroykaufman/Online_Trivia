##############################################################################
# client.py
##############################################################################
import chatlib  # To use chatlib functions or consts, use chatlib
import socket

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client, localhost
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
	"""
	Builds a new message using chatlib, wanted code and message. 
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
	full_msg = chatlib.build_message(code,data)
	conn.send(full_msg.encode())
	print(full_msg)

def recv_message_and_parse(conn):
	"""
	Recieves a new message from given socket,
	then parses the message using chatlib.
	Paramaters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message. 
	If error occured, will return None, None
	"""
	full_msg = conn.recv(1024).decode()#recve a msg and decoed it.
	cmd, data = chatlib.parse_message(full_msg)
	return cmd, data
	
	

def connect():#function for conacting to the server by socket
	conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)# first parameter say that we using IP for cimunication the secund parmeter say that we using tcp for strming data.
	conn.connect((SERVER_IP,SERVER_PORT))# creat socket on localhost
	return conn


def error_and_exit(error_msg):
    print(error_msg)
    exit()

def build_send_recv_parse(conn,cmd,data):
	#send a message and wait for answare that contain comend and data
	build_and_send_message(conn,cmd,data)
	return recv_message_and_parse(conn)
	

def get_score(conn):
	"""
	Send request for user score.
	Recieve: socket
	Return: -
	"""
	cmd,score = build_send_recv_parse(conn,chatlib.PROTOCOL_CLIENT["get_score"],"")
	if cmd!="YOUR_SCORE":
		return error_and_exit("error")
	return score
def get_highscore(conn):
	"""
	Send request for get all user's scores from high to low.
	Recieve: socket
	Return: score users.
	"""
	cmd,scoretable = build_send_recv_parse(conn,chatlib.PROTOCOL_CLIENT["high_score_table"],"")
	if cmd!="ALL_SCORE":
		return error_and_exit("error")
	return scoretable


def login(conn):#send login recuest until user login
	cmd=""
	while cmd!="LOGIN_OK":
		
	    username = input("Please enter username: \n")
	    password = input("password: \n")
	    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"],username+"#"+password)
	    cmd,data = recv_message_and_parse(conn)
	    if cmd!="LOGIN_OK":
	    	print("password or username incourect" )



def logout(conn):
	#send logout recuest
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"],"")

def play_quation(conn):
	"""
	Send request to get quation, and wait to recieve answer.
	Recivev: socket
	Return: -
	"""
	cmd,quation = build_send_recv_parse(conn,chatlib.PROTOCOL_CLIENT["aske_for_quation"],"")
	if cmd=="NO_QUESTIONS":
		print("GAME OVER")
		return None
	elif cmd=="YOUR_QUESTION":
		quation_part = quation.split("#")#split every part of the quation,id,quation and option
		print(quation_part)
		print(quation_part[1]+"\n"+"1: "+quation_part[2]+"\n"+"2: "+quation_part[3]+"\n"+"3: "+quation_part[4]+"\n"+"4: "+quation_part[5]+"\n")

	user_answer = input("enter one of the folowing option: ")
	cw,answer = build_send_recv_parse(conn,chatlib.PROTOCOL_CLIENT["send_answer"],quation_part[0]+"#"+user_answer)#retuen the corect answer and corect or wrong
	print(cw)
	if cw=="CORRECT_ANSWER":
		print("correct!, good job")
	elif cw == "WRONG_ANSWER":
		print("wrong the answer is: ",answer)


def get_logged_users(conn):
	# Send request for all user's that login
	cmd,users = build_send_recv_parse(conn,chatlib.PROTOCOL_CLIENT["login_user"],"")
	print(users)



def main():
    conn = connect()
    login(conn)
    recuest_code=""
    while recuest_code!="5":
	    recuest_code = input(" 1 for high score table\n 2 for your score \n 3 for start playing \n 4 for login users \n 5 to logout \n : ")
	    if recuest_code=="1":
	    	print(get_highscore(conn))
	    if recuest_code=="2":
	    	print(get_score(conn))
	    if recuest_code=="5":
	    	logout(conn)
	    if recuest_code=="3":
	    	play_quation(conn)
	    if recuest_code=="4":
	    	get_logged_users(conn)
    conn.close()

if __name__ == '__main__':
    main()
