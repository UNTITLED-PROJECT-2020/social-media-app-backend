# **Chat** Documentation

## HTTP Endpoints
All the endpoints in the chat app, that help us to get/update/delete
various amounts of data abstractions in out backend. 

Most of these have some kind of error handling. and can have 
mutiple kinds of responses depending upon the request and type 
of request

The general analogy of the type of request sent is:

get ==> list
post ==> create
put ==> update
patch ==> retrieve
delete ==> delete

**end-points:**
***Template Files for Testing***
- `http://127.0.0.1:8000/chat`
- `http://127.0.0.1:8000/chat/personal/<msg_from>/<msg_to>/`
- `http://127.0.0.1:8000/chat/group/<msg_from>/<grp>`
- `http://127.0.0.1:8000/chat/room/<msg_from>/<room_name>`

======================================================================================================

### ***Create Specific Chats or Upgrade chats***
- `http://127.0.0.1:8000/chat/special`

<--TODO : (Implement)-->

- `http://127.0.0.1:8000/chat/special/personal`

On this endpoint we can create or delete a dialogue for 2 people
for any to users to use personal chats, they need to have dialogues.

Every single conversation has 2 dialogues, where the roles of 
sender and receiver are interchanged between the 2 people.

If the contact you were searching for was not found then a
`"detail": "Not found."` 404 NOT FOUND response is sent back 

#### POST

Sending the below POST request automatically creates both the
dialogues. Hence, no need to send 2 POST requests.

There are 2 possible response, if these dialogues do not exist,
then in the "info" field of the response.data has the word "created"
in it. 

If the dialogues already exist then ther is no need to 
create new ones, hence if a conversation already exits then 
the "info" field of the response.data has the word "returned"

```py
request:
  {
  	"msg_from": "9797979797",
  	"msg_to": "9999999999"
  }
  
response:
  {
    "msg_from": "9797979797",
    "msg_to": "9999999999",
    "info": "created"
  }
  
OR

response:
  {
      "msg_from": "9797979797",
      "msg_to": "9999999999",
      "info": "returned"
  }
  
      OR
response:
  {
      "detail": "Not found."
  }
```


#### Delete

Sending a DELETE request deletes both the dialogues and
also all the saved messages related to that database

```py
request:
  {
  	"msg_from": "9797979797",
  	"msg_to": "9999999999"
  }
  
response:
  {
      "msg_from": [
          1,
          {
              "chat.Message": 0,
              "chat.Dialogue": 1
          }
      ],
      "msg_to": [
          1,
          {
              "chat.Message": 0,
              "chat.Dialogue": 1
          }
      ],
      "info": "deleted",
      "message": "Chat Deleted"
  }

      OR
response:
  {
      "detail": "Not found."
  }
```


- `http://127.0.0.1:8000/chat/special/group`

On this endpoint we can create/delete/update a group for 2 or more people
for any to users to use group chats, they need to be in a group.

Every single conversation has admins and participants, the admins
are a subset of all the participants in a group

If the contact you were searching for was not found then a
`"info": "error"` 400 BAD REQUEST response is sent back 

#### POST

Sending the below POST request creates a group if the
phone number of the admin is not present in the participants
it is automatically added, but this method is not recommended.

the returned response has 2 extra fields of `info` and `key`,
the key is VERY important as using that 10 charater long unique
string we can access and send messages to that group.

Also, the fiels like name and bio are limited to 30 and 80
charaters respectively.

```py
request:
  {
  	"name": "Untitled Project",
  	"bio": "we are the best",
  	"admin": ["9999999999"],
  	"participants": ["9797979797", "9898989898"]
  }
  
response:
  {
      "name": "Untitled Project",
      "key": "1E0C652D78",
      "bio": "we are the best",
      "participants": ["9797979797","9898989898","9999999999"],
      "admin": ["9999999999"],
      "info": "created"
  }

    OR

response:
{
    "message": {
        "participants": ["Object with ph_num=87878 does not exist."]
        "admin": ["Object with ph_num=112211 does not exist."]
    },
    "info": "error"
}
```



#### PATCH

Sending the below PATCH requests updated an existing group
these methods are used for `adding/removing/promting` participants,
these actions can only be performed by admins, whereas the
`leave` can be executed by anyone.

*ADD*

Here the admin is adding a new user to the group, 
maximum limit of participants in a group is 128
members initially

```py
request:
  {
  	"command" : "add",
  	"key": "B5CD1D81DF7",
  	"msg_from": "9797979797",
  	"msg_to": "1123456789"
  }
  
response:
  {
      "info": "added",
      "message": "The user has been added sucessfully"
  }
      OR
response:
  {
      "detail": "Not found."
  }
    OR
response:
  {
      "info": "error",
      "message": "The Sender is not an Admin"
  }
    OR
response:
  {
      "info": "error",
      "message": "Group Full"
  }
```

*REMOVE*

Here the admin is removing a participant from the group, 
this can only be done by an admin to a participant and 
the same removed user can be added again.

```py
request:
  {
  	"command" : "remove",
  	"key": "1E0C652D78",
  	"msg_from": "9999999999",
  	"msg_to": "1123456789"
  }
  
response:
  {
      "info": "removed",
      "message": "The user has been removed sucessfully"
  }

response:
  {
      "info": "error",
      "message": "Wrong Operation"
  }
```

*PROMOTE*

Here an admin promotes a participant from the group, 
to Admin authorization, once made Admin, he cannot be 
removed as admin or from the group and has the ability 
to add/remove/promote other participants.

```py
request:
  {
  	"command" : "promote",
  	"key": "1E0C652D78",
  	"msg_from": "9999999999",
  	"msg_to": "1123456789"
  }
  
response:
  {
      "info": "promoted",
      "message": "The user has been promoted sucessfully"
  }
```

*LEAVE*

Here a user basically exits from the group and can be added
again. If an admin leaves, he is removed from both the admin 
and participants field. 

If the only admin in the group levaes then a random participant
is atuomatically promoted to admin.

if participants reach 0, then the group is automatically 
deleted with all the messages linked to it are also erased.

request:
```py
  {
  	"command" : "leave",
  	"key": "1E0C652D78",
  	"msg_from": "1123456789"
  }
  
response:
  {
      "info": "left",
      "message": "the user has left the group"
  }
```

- `http://127.0.0.1:8000/chat/special/room`

<--TODO : (Implement)-->

======================================================================================================

### ***Retreving/Updating Chat information***
- `http://127.0.0.1:8000/chat/info`

<--TODO : (Implement)-->

- `http://127.0.0.1:8000/chat/info/active`

This endpoint is specifically created to retrieve/update 
information about a users activity, 

If the user is online then showing him as active and if 
the user is ofline then when was the last time that he 
was online

This information can be displayed over personal chatboxes

#### PATCH

This method simply retrieves the acitive details of a
user from his phone number

```py
request:
  {
  	"user_num": "9999999999"
  }
  
response:
  {
      "info": "found",
      "active": false,
      "last_active": "2020-11-02T13:26:44Z"
  }
      OR
response:
  {
      "info": "found",
      "active": true,
      "last_active": "2020-11-02T13:26:44Z"
  }
      OR
response:
  {
      "detail": "Not found."
  }
```

#### PUT

This method simply updates the acitive details of a
user , this is updated when a user open the app, or
when he closes his app.

```py
request:
{
	"user_num": "9999999999",
	"command" : "activate",
	"last_active": "2020-11-25 07:36:50"
}

request:
{
	"user_num": "9999999999",
	"command" : "deactivate",
	"last_active": "2020-11-25 07:36:50"
}

response:
  {
      "info": "updated",
      "message": "Active Data Has been updated"
  }
  
      OR
	  
response:
  {
      "info": "error",
      "message": "incorrect request/url"
  }
  
        OR
		
response:
  {
      "detail": "Not found."
  }
```



- `http://127.0.0.1:8000/chat/info/personal`

This endpoint is specifically created to retrieve 
information about a personal chat that the use is in, 

This information can be displayed over personal chatboxes
details and refreshed everytime the user opens the info part

#### PATCH

This method simply retrieves the personal chat details 
of a user from his phone number

```py
request:
  {
  	"msg_from": "9797979797",
  	"msg_to": "9898989898"
  }
  
response:
  {
      "last_received_receiver": "2020-10-30T18:54:59.433Z",
      "last_seen_receiver": "2020-10-28T18:39:02.136Z",
      "info": "returned"
  }
      OR
response:
  {
      "detail": "Not found."
  }
```


- `http://127.0.0.1:8000/chat/info/group`

This endpoint is specifically created to retrieve 
information about a group chat that the use is in, 

This information can be displayed over group chatboxes
details and refreshed everytime the user opens the info part

these can be used to check if a user have been removed from
a group, or he has been made admin etc.

#### PATCH

This method simply retrieves the group chat details 
of a group using the key of that group

```py
request:
  {
  	"grp_name": "1E0C652D78"
  }
  
response:
  {
      "name": "Untitled Project",
      "key": "1E0C652D78",
      "bio": "we are the best",
      "participants": ["9797979797","9898989898","9999999999"],
      "admin": ["9999999999"],
      "info": "created"
  }
      OR
response:
  {
      "detail": "Not found."
  }
```

- `http://127.0.0.1:8000/chat/info/room` 

<--TODO : (Implement)-->

======================================================================================================

  
## WSS Endponts
The reciever socket is meant to get all messages at a global level, It is
dynamically created by interpolating the value of the users phone number 
in place of **'msg_from'**
- chatReceiveSocket = `'wss://' + window.location.host + '/ws/chat/special/' + msg_from + '/'`

The personal message send socket is meant to send specific messages at an 
instance level (i.e. the currently opened chatbox), It is dynamically 
created by interpolating the value of the user's phone number in place of 
**'msg_from'** and the value of the phone number to whome the user wants to
send the message to in place of **'msg_to'**
- chatSendSocket = `'wss://' + window.location.host + '/ws/chat/personal/' + msg_from + '/' + msg_to + '/'`

The group message send socket is meant to broadcast specific messages at an 
instance level (i.e. the currently opened chatbox), It is dynamically 
created by interpolating the value of the user's phone number in place of 
**'msg_from'** and the value of the key of the group to whome the user wants 
to send the message to in place of **'grp'**
- groupSendSocket = `'wss://' + window.location.host + '/ws/chat/group/' + msg_from + '/' + grp + '/'`


***NOTE : THE JSON THAT IS RECEIVED FROM THE 'chatReceiveSocket' MAY HAVE***
***VARIABLE VALUES, BUT THE INPUT JSON IN 'chatSendSocket' AND 'groupSendSocket'***
***ALWAYS AHBE SPECIFIC JSON FIELDS, THESE ARE :***
***['message', 'msg_from', 'msg_to', 'command', 'sent_timestamp']***

======================================================================================================

### Personal Message Commands
Here we implement the discoarse between 2 unique users. This is
achieved by the 10-digit phone numbers of each user that is linked
to their account. Every conversation has 2 Dialogues, each in which
one user is the **sender** and the other is the **receiver**.

Each message that is sent also, is saved in case the receive is
offline. So that the message can be retrieved later and after
storing locally a 'msg_recived' response could be sent which 
deletes the message instance on the server freeing space.

---

`new_msg`
In this command the sender send a new message to the
receiver, the sent message is saved in the database.

Aftr saving the message, the sender gets back a response
of "msg_sent", signifying that the backend has received and 
saved this message sucessfully but it has still not receached
the receiver.


expected input [ in chatSendSocket.send() ] :
```py
  {
      'message': 'ok',                                      // message content
      'command': 'new_msg',                                 // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 16:32:17.356'           // datetime at which the 'new_msg' command was sent
  }
```

expected output [ in chatReceiveSocket.onmessage() ] :
```py
  {
      'message': 'ok',                                      // message content
      'command': 'new_msg',                                 // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 16:32:17.356'           // datetime at which the 'new_msg' command was sent
  }
```

expected output [ in chatSendSocket.onmessage() ] :
```py
  {
      'message': '2020-11-21 16:32:17.356',                 // datetime at which the 'new_msg' command was sent
      'command': 'msg_sent',                                // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 16:32:18.789'           // datetime at which the 'msg_sent' command was sent
  }
```

---

`msg_received`
In this command the sender sends a message to the
receiver, infering that an earlier message that was
sent (by the receiver in this case) has been received 
and stored locally.

This method also updates the ***last_received_receiver***
field in the Dialogue of the Sender using the
***'sent_timestamp'*** field in the input

**NOTE : EXECUTING THIS COMMAND WILL DELETE THE SAVED MESSAGE**
**INSTANCE IN THE DATABASE, AND WOULD NOT BE AVAILABLE FOR FETCH.**
**HENCE,ONLY SEND THIS MESSAGE WHEN YOU ARE SURE THAT THE MESSAGE**
**HAS BEEN STORED LOCALLY**


expected input [ in chatSendSocket.send() ] :
```py
  {
      'message': '2020-11-21 17:11:06.23',                  // datetime at which the 'new_msg' command was sent
      'command': 'msg_received',                            // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'msg_received' command was sent
  }
```

expected output [ in chatReceiveSocket.onmessage() ] :
```py
  {
      'message': '2020-11-21 17:11:06.23',                  // datetime at which the 'new_msg' command was sent
      'command': 'msg_received',                            // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'msg_received' command was sent
  }
```

---

`msg_read`
In this command the sender sends a message to the
receiver, infering that an earlier message that was
sent (by the receiver in this case) has been read
by the sender.

This method also updates the ***last_seen_receiver***
field in the Dialogue of the Sender using the
***'sent_timestamp'*** field in the input


expected input [ in chatSendSocket.send() ] :
```py
  {
      'message': '2020-11-21 17:11:06.23',                  // datetime at which the 'new_msg' command was sent
      'command': 'msg_read',                                // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'msg_read' command was sent
  }
```

expected output [ in chatReceiveSocket.onmessage() ] :
```py
  {
      'message': '2020-11-21 17:11:06.23',                  // datetime at which the 'new_msg' command was sent
      'command': 'msg_read',                                // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'msg_read' command was sent
  }
```

---

`is_typing`
In this command the sender sends a message to the
receiver, infering that he/she is typing a message
right-now.

This message is to be displayed temporaryly at the
side of the receiver (2 seconds maybe). Also, this 
command should be sent by the sender occasionally,
(every 2-3 secons) while typing a message.


expected input [ in chatSendSocket.send() ] :
```py
  {
      'message': '-null-',                                  // empty message
      'command': 'is_typing',                               // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'is_typing' command was sent
  }
```

expected output [ in chatReceiveSocket.onmessage() ] :
```py
  {
      'command': 'is_typing',                               // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'is_typing' command was sent
  }
```

---

`error`
Sometimes an error may occor in authentication,
or any of the above given command, in that case.
specific error cases will be sent back to the receiver
so that the problem may be corrected or tried again.

The **'command'** in these messages are always **'error'**,
but **'type'** may change to denote the specific process 
in which this process occured. Hence, 2 nested **'if'**
conditions can be used to handle this.

expected output [ in chatSendSocket.onmessage() ] :
```py
  {
      'message': "couldn't find a message to delete",       // error message
      'command': 'error',                                   // error command 
      'type': 'delete_msg'                                  // command during which error occured
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'error' command was sent
  }
```
<!-- TODO: (Add All error cases) -->
======================================================================================================

### Group Message Commands
Here we implement the discoarse between 2 or more unique users. This 
is achieved by the 10-digit phone numbers of each user that is linked
through a many-to-many field to a Group which has a 10-digit unique 
key. Every conversation has a Group instances, in which users is that 
group are refenced as **participants** and a subset of the participants 
that have higher authority are the **admin**.

Each message that is sent also, is saved in case some of the 
receivers are offline. So that the group messages can be retrieved 
later and after storing locally a 'msg_recived' response could be 
sent which removes the specific user from the **'pending'** field
in the message instance on the server, and if a user is the last one
to receive a message (i.e. pending is 1), we delete the message freeing 
space.

All commands on the side of ***chatReceiveSocket.onmessage()*** are more
or less the same, they will just be broadcasted to multiple users.
But, the commands on the side of ***chatSendSocket.send()*** deviate
heavily.

---

`new_grp_msg`
In this command the sender broadcasts a new message to 
all the receivers, the sent message is saved in the 
database.

Aftr saving the message, the sender gets back a response
of "msg_sent", signifying that the backend has received and 
saved this message sucessfully but it has still not receached
the receiver.


expected input [ in chatSendSocket.send() ] :
```py
  {
      'message': 'ok',                                      // message content
      'command': 'new_grp_msg',                             // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': 'test12test',                               // key of the group receiving the msg
      'sent_timestamp': '2020-11-21 16:32:17.356'           // datetime at which the 'new_grp_msg' command was sent
  }
```

expected output [ in chatReceiveSocket.onmessage() ] :
```py
  {
      'message': 'ok',                                      // message content
      'command': 'new_msg',                                 // command to be executed
      'msg_from': 'test12test-9999999999',                  // group key and phone num of the sender ('-' separated)
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 16:32:17.356'           // datetime at which the 'new_grp_msg' command was sent
  }
```

expected output [ in chatSendSocket.onmessage() ] :
```py
  {
      'message': '2020-11-21T16:32:17.356Z',                // datetime at which the 'new_grp_msg' command was sent
      'command': 'msg_sent',                                // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 16:32:18.789'           // datetime at which the 'msg_sent' command was sent
  }
```

---

`grp_msg_received`
In this command the sender sends a message to the
receiver, infering that an earlier message that was
sent (by the receiver in this case) has been received 
and stored locally.

This method also updates the ***last_received_receiver***
field in the Dialogue of the Sender using the
***'sent_timestamp'*** field in the input

**NOTE : EXECUTING THIS COMMAND WILL DELETE THE SAVED MESSAGE**
**INSTANCE IN THE DATABASE, AND WOULD NOT BE AVAILABLE FOR FETCH.**
**HENCE,ONLY SEND THIS MESSAGE WHEN YOU ARE SURE THAT THE MESSAGE**
**HAS BEEN STORED LOCALLY**


expected input [ in chatSendSocket.send() ] :
```py
  {
      'message': '2020-11-21T17:11:06.23Z',                 // datetime at which the 'new_grp_msg' command was sent
      'command': 'grp_msg_received',                        // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'grp_msg_received' command was sent
  }
```

expected output [ in chatReceiveSocket.onmessage() ] :
```py
  {
      'message': '2020-11-21T17:11:06.23Z',                 // datetime at which the 'new_grp_msg' command was sent
      'command': 'msg_received',                            // command to be executed
      'msg_from': 'test12test-9999999999',                  // group key and phone num of the sender ('-' separated)
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'grp_msg_received' command was sent
  }
```

---

`grp_msg_read`
In this command the sender sends a message to the
receiver, infering that an earlier message that was
sent (by the receiver in this case) has been read
by the sender.

This method also updates the ***last_seen_receiver***
field in the Dialogue of the Sender using the
***'sent_timestamp'*** field in the input


expected input [ in chatSendSocket.send() ] :
```py
  {
      'message': '2020-11-21 17:11:06.23',                  // datetime at which the 'new_grp_msg' command was sent
      'command': 'msg_read',                                // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'grp_msg_read' command was sent
  }
```

expected output [ in chatReceiveSocket.onmessage() ] :
```py
  {
      'message': '2020-11-21 17:11:06.23',                  // datetime at which the 'new_grp_msg' command was sent
      'command': 'msg_read',                                // command to be executed
      'msg_from': 'test12test-9999999999',                  // group key and phone num of the sender ('-' separated)
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'grp_msg_read' command was sent
  }
```

---

`is_grp_typing`
In this command the sender sends a message to the
receiver, infering that he/she is typing a message
right-now.

This message is to be displayed temporaryly at the
side of the receiver (2 seconds maybe). Also, this 
command should be sent by the sender occasionally,
(every 2-3 secons) while typing a message.


expected input [ in chatSendSocket.send() ] :
```py
  {
      'message': '--null--',                                // empty message
      'command': 'is_grp_typing',                           // command to be executed
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'is_grp_typing' command was sent
  }
```

expected output [ in chatReceiveSocket.onmessage() ] :
```py
  {
      'command': 'is_typing',                               // command to be executed
      'msg_from': 'test12test-9999999999',                  // group key and phone num of the sender ('-' separated)
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'is_grp_typing' command was sent
  }
```

---

`error`
Sometimes an error may occor in authentication,
or any of the above given command, in that case.
specific error cases will be sent back to the receiver
so that the problem may be corrected or tried again.

The **'command'** in these messages are always **'error'**,
but **'type'** may change to denote the specific process 
in which this process occured. Hence, 2 nested **'if'**
conditions can be used to handle this.

expected output [ in chatSendSocket.onmessage() ] :
```py
  {
      'message': "couldn't find a message to delete",       // error message
      'command': 'error',                                   // error command 
      'type': 'delete_msg'                                  // command during which error occured
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'error' command was sent
  }
```
<!-- TODO: (Add All error cases) -->

======================================================================================================
### Room Message Commands

======================================================================================================
### Special Message Commands
there are some commands that are only defined for 
**chatReceiveSocket**, these are primaryly methods to
get back data from the server that has not yet been 
saved locally.

---

`fetch_msgs`
In this command the sender sends a message to the
receiver, infering that an earlier message that was
sent (by the receiver in this case) has been received 
and stored locally.


expected input [ in chatReceiveSocket.send() ] :
```py
  {
      'message': '--null--',                                // empty message
      'command': 'fetch_msgs',                              // command to be executed
      'msg_from': '9797979797',                             // **(dosent matter actually)**
      'msg_to': '9999999999',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'fetch_grp_msgs' command was sent
  }
```

expected output [ in chatReceiveSocket.onmessage() ] :
```py
  {
    "command": "fetch_msgs",                                    // command to be executed
    "all": "True"                                               // specifying if it is the last chunk of messages
    "messages": [                                               // messages array (empty on no new message)
        {
          "msg_from": "9797979797", 
          "msg_to": "9999999999", 
          "message": "zzz", 
          "command": "new_msg", 
          "sent_timestamp": "2020-11-19T17:56:03.880000Z", 
        }, 
        {
          "msg_from": "9898989898", 
          "msg_to": "9999999999", 
          "message": "ok", 
          "command": "new_msg", 
          "sent_timestamp": "2020-11-22T08:50:01.670000Z", 
        }
      ]
  }
```

---

`fetch_grp_msgs`
In this command the sender sends a message to the
receiver, infering that an earlier message that was
sent (by the receiver in this case) has been received 
and stored locally.


expected input [ in chatReceiveSocket.send() ] :
```py
  {
      'message': '--null--',                                // empty message
      'command': 'fetch_grp_msgs',                          // command to be executed
      'msg_from': 'test12test',                             // **(dosent matter actually)**
      'msg_to': '9999999999',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'fetch_grp_msgs' command was sent
  }
```

expected output [ in chatReceiveSocket.onmessage() ] :
```py
  {
    "command": "fetch_grp_msgs",                                // command to be executed
    "all": "False"                                              // specifying if it is the last chunk of messages
    "messages": [                                               // messages array (empty on no new message)
        {
          "msg_from": "test12test-9797979797", 
          "msg_to": "9999999999", 
          "message": "new", 
          "command": "new_msg", 
          "sent_timestamp": "2020-11-19T17:56:03.880000Z", 
          "pending": ["9999999999"]                             // group participants who have not received the message
        }, 
        {
          "msg_from": "test12test-9898989898", 
          "msg_to": "9999999999", 
          "message": "ok", 
          "command": "new_msg", 
          "sent_timestamp": "2020-11-22T08:50:01.670000Z", 
          "pending": ["9797979797", "9999999999"]               // group participants who have not received the message
        }
      ]
  }
```

---

`error`
Sometimes an error may occor in authentication,
or any of the above given command, in that case.
specific error cases will be sent back to the receiver
so that the problem may be corrected or tried again.

The **'command'** in these messages are always **'error'**,
but **'type'** may change to denote the specific process 
in which this process occured. Hence, 2 nested **'if'**
conditions can be used to handle this.

expected output [ in chatSendSocket.onmessage() ] :
```py
  {
      'message': "couldn't find a message to delete",       // error message
      'command': 'error',                                   // error command 
      'type': 'delete_msg'                                  // command during which error occured
      'msg_from': '9999999999',                             // phone num of the person sending the msg
      'msg_to': '9898989898',                               // phone num of the person receiving the msg
      'sent_timestamp': '2020-11-21 17:11:30.404'           // datetime at which the 'error' command was sent
  }
```
<!-- TODO: (Add All error cases) -->

======================================================================================================
