# Online Trivia
## Description
A fun litel trivia game that multipal user can join the server and play.

## Instraction for player
1. Run the server.py,this file setup the server. 
2. Run clinet.py.
3. Now you need to login,ther isn't any option to singin yat so I'll leve 3 users.
4. After login the main menu show up and you can writ 5 comend.
5. From her you can play and follow the instraction.

---
# Application protocol
## Messege
CCCCCCCCCCCCCCCC|LLLL | MMM\
**c** - represent the commend of the claient.\
**L** - represend the messege length.\
**M** - represend client messege.
## client -> server
**Singin request** = LOGIN           |0000|**UserName#Password**\
**logout request** = LOGOUT          |0000|\
**request for all online users** = LOGGED          |0000|\
**request for a trivia quation** = GET_QUESTION    |0000|\
**Send answer** = SEND_ANSWER     |0003|quation number#chosen answer\
**Send request for users score** = MY_SCORE        |0000| \
**Send request for the all users scores from high to low** = HIGHSCORE       |0000|
## server -> client
**Aprove messege for login** = LOGIN_OK        |0000|\
**Send list of all users that logged** = LOGGED_ANSWER   |0004|**user1, user2**\
**Send a random quation** = YOUR_QUESTION   |0000|**quation number#quation#a1#a2#a3#a4**\
**Currect answer ** = CORRECT_ANSWER  |0000|\
**wrong answer** = WEONG_ANSWER  |0001|**currect answer**\
** send user score** = WEONG_ANSWER  |0001|**score**\
** Send all users score from high to low** = ALL_SCORE       |0000|**user1: score\n user2: score**\
** erreo messege** = ERROR|0000|**error description**\

---
# Project status
The project now just do a simple things and work only on LAN network.\
feel free to upgrade and add may things as you like, I'll be more then happy to help with any thing.

