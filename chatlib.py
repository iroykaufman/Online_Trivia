# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT",
"get_score" : "MY_SCORE",
"high_score_table" : "HIGHSCORE",
"aske_for_quation" : "GET_QUESTION",
"send_answer" : "SEND_ANSWER",
"login_user" : "LOGGED"
} 


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR",
"error_message" : "ERROR",
"login_ok" : "LOGIN_OK",
"send_score" : "YOUR_SCORE",
"send_all_score" : "ALL_SCORE",
"send_login_users" : "LOGGED_ANSWER",
"send_quation" : "YOUR_QUESTION",
"currect" : "CORRECT_ANSWER",
"wrong" : "WRONG_ANSWER"

} 


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
	if len(cmd)>16 or len(data)>9999:
		return None
	spaces='                '
	zeos="0000"
	full_msg=cmd +spaces[0:16-len(cmd)]+"|"+zeos[0:4-len(str(len(data)))]+ str(len(data))+"|"+data

	return full_msg


def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
	List=list(data.split('|')) #creat list of the msg
	
	# inital check for the data
	if len(List)<=2 :
		return None,None
	if len(List[1])!=4 or containletter(List[1]):
		return None,None


	if int(List[1])==len(List[2]):
		msg=List[2]
	else:
		return None,None
	
	if len(List[0])>16:
		return None,None
	cmd=List[0].replace(' ','')
	return cmd, msg

def expected_fields(data):
	"""return the expected length field"""
	l = list(data.split('|')) #creat list of the msg
	return int(l[1])


def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	count=0
	List=[]
	temp_str=""
	for x in msg:
		
		if x=="#":
			count+=1
			List.append(temp_str)
			temp_str=""
		else:
			temp_str=temp_str+x

	if count==expected_fields:
		List.append(temp_str)
		return List
	else:
		return [None]




def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	return "#" .join(map(str,msg_fields))

def containletter(string):
	for x in string:
		if x.isalpha():
			return True

	return False
