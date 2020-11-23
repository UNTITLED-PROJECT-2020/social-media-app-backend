# **Chat** Documentation

## HTTP Endpoints
All the endpoints in the  

**end-points:**
***Template Files for Testing***
- `http://127.0.0.1:8000/chat`
- `http://127.0.0.1:8000/chat/personal/<msg_from>/<msg_to>/`
- `http://127.0.0.1:8000/chat/group/<msg_from>/<grp>`
- `http://127.0.0.1:8000/chat/room/<room_name>`

***Create Specific Chats or Upgrade chats***
- `http://127.0.0.1:8000/chat/special`
- `http://127.0.0.1:8000/chat/special/personal`
- `http://127.0.0.1:8000/chat/special/group`
- `http://127.0.0.1:8000/chat/special/room`

***Retreving/Updating Chat information***
- `http://127.0.0.1:8000/chat/info`
- `http://127.0.0.1:8000/chat/info/personal`
- `http://127.0.0.1:8000/chat/info/group`
- `http://127.0.0.1:8000/chat/info/room` 
  
## WSS Endponts
The reciever socket is meant to get all messages at a global level, It is
dynamically created by interpolating the value of the user's phone number 
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

====================================================================================
====================================================================================

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
====================================================================================
====================================================================================

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
group, infering that an earlier message that was
sent (by the receiver in this case) has been read
by the sender.


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
group, infering that he/she is typing a message
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

====================================================================================
====================================================================================
### Room Message Commands

====================================================================================
====================================================================================
### Special Message Commands
there are some commands that are only defined for 
**chatReceiveSocket**, these are primaryly methods to
get back data from the server that has not yet been 
saved locally.

---

`fetch_msgs`

In this command the receiver sends a message to the
backend server, to fetch all the personal messages that
may have been received by the user while he was offline.

After fetching these messsages can be saved locally and
the a 'msg_received' comand could be sent automatically
to delete all these instances and free up space online


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

In this command the receiver sends a message to the
backend server, to fetch all the group messages that
may have been received by the user while he was offline.

After fetching these messsages can be saved locally and
the a 'grp_msg_received' comand could be sent automatically
to delete all these instances and free up space online


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

====================================================================================
====================================================================================
