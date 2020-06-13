# Overview
 
 200 : Success / Request is success<br>
 201 : Created<br>
 203 : Accepted<br>
 205 : Acknowledge<br>
 400 : Invalid Request Syntax / Bad Request<br>
 401 : Not Approved<br>
 411 : Unknown Request / Invalid Request<br>
 305 : Member Busy<br>
 415 : Unsupported media format<br>
 404 : Member not found<br>
 412 : Invalid Request argument/s<br>
 406 : Request rejected<br>
 500 : Internal error<br>


#### TRACKER AND MEMBER

#### REQUESTING LIST_OF_MEMBERS [MEMBER]>[TRACKER_SERVER]

LIST OF MEMBERS: This protocol is used by Member in order to request updated member list from Tracker Server.

Note: Format used below: [from]>>[to]. This describes the message sent by [from] to
the [to].

 Request -

#### LIST_

 Response:

[res_code] [list.of.members] [count]

o variables description
 200 : Response code
 List of Members: List of member objects in JSONFormat this JSON object contains data of all active members with following Keys
( member.ip and member_port / socket.number ).

#### 2. REGISTER MEMBER TO THE CHEESE_STACK_SYSTEM [MEMBER]>[TRACKER_SERVER]

This protocol is used by the Member to register itself on the tracker server as a Member of Cheese
Stack System.

 Request

REGISTER_Mem [mem.ip] [mem.port]

1. mem.ip : IP of the member.
2. mem.port: Port number of the member where CHEESE STACK
SYSTEM process running.
 Response

[res_code]

Ex: 201 - CREATED

### 3. LIVELINESS_PING [TRACKER_SERVER]>[MEMBER]

LIVELINESS_PING protocol is used by Tracker server in order to assure the availability of the
members in the network.

 Request

#### PING_TS


 Response

[res_code]

Ex: 200 - SUCCESS

# Member to Member (Peer to Peer) Communication

Below section discuss protocol used in member to member communication.

In this section, we describe all request and its format send by member and
corresponding response and its format returned by another member to the
requested member. Additionally we describe contents of the requests and the responses.

Note: Format used below: [from]>>[to]. This describes the message sent by [from] to
the [to].

#### 1. REQUESTING CHEESE STACK [NEW_MEMBER]>[MEMBER]

This protocol is been followed by new member of Cheese Stack System, in order to get complete
chain of Cheese.Stack. New member will select one of the existing member randomly and send
request for Cheese.Stack.

 Request

#### REQ.CHEESE.STACK

 Response

[res_code] CHEESE.STACK

#### 2. SHARE TRANSACTION [MEMBER]>[MEMBER]

This Protocol is followed by Member in order to share new transaction details to other
active Member/s for the process of PROOF OF WORK.

 Request

NEW_TRAN [sequence.no]

o This request will send to all the active members of the network to inform about
new transaction
o sequenc_no: This argument will be send to all members. So, they can use this id when they requesting back for transaction details. Also, this number can be used to check, whether already transaction details received or not.<br><br>
 Response

[res.code]


o acknowledge: Receiver member acknowledged to the sender member. Ex
: [205]

#### 3. REQUEST NEW TRANSACTION DETAILS [MEMBER]>[MEMBER]

This Protocol is followed by Member in order to request new transaction details from other
member who had already send new transaction notification.

 Request

REQ.TRAN [sequence.no]

1. transaction.id: is used to get exact transaction information from the member
who send NEW_TRAN request
 Response

[res.code] [new.transaction.details]

2. new_transaction.details: Details of the new transaction.

#### 3. BROAD CAST NEW CHEESE [MEMBER]>[MEMBER]

This protocol will be followed by all the members of CHEESES.COIN.SYSTEM, in terms of broadcasting new block to the network. Whenever a Member created a new Cheese, they will broadcast that new Cheese to all other member for the purpose of validation.

 Request

NEW.CHEESE.CREATED [cheese_id]

1. This request will send to all the active members of the network to inform about
newly created cheese.
2. NEW_CHEESE: This request notify or inform other members that new cheese
has been created and it is ready for Validation.
3. Cheese_id: This argument will be send to the all members. So, they can use this
id when they requesting back for new cheese details. Also, this id can be used to
check, whether already cheese details received or not.
 Response

[res_code]

o acknowledge: Receiver member acknowledged to the sender member. Ex
: [205]

#### 4. REQUESTING NEW CHEESE DATA [MEMBER]>[MEMBER]

This protocol will be followed by all the members of CHEESES.COIN.SYSTEM, for the
purpose of requesting NEW CHEESE data which they already notified. After, they can perform
process of Validation.


 Request

REQ.NEW.CHEESE [cheese_id]

1. cheese_id: is used to get exact new cheese data from the member who send NEW.CHEESE.CREATED request.<br><br>

 Response

[res.code] [cheese.data] [nonce] [member.id]

2. cheese.data: This object will contains all the details of the new cheese. It
contains set of key, value pairs.
3. nonce: This will be shared along with cheese_data. So that, other members
can validate easily.
4. member_id: This will be used to send validation data to creator of the NEW
CHEESE.

#### 5. UPDATE CHEESE STACK [MEMBER]>[MEMBER]

This protocol is been followed by all the members of the Cheese Stack System, in order to
synchronize the Cheese_Stack. New member will select 5 Members of
from MEMBERS.LIST and send request.

 Request

 UPD.CHEESE.STACK

 Response

[res_code] CHEESE.STACK

o Members will use this CHEESE.STACK and compare with their local cheese
stack. They will update their cheese stack, if there is a difference

### REQUESTING VALIDATION DATA [MEMBER]>[MEMBER]

This protocol will be followed by all the members of CHEESES.COIN.SYSTEM, for the
purpose of requesting Validation data which they already created. So the creator of NEW
CHEESE can add new cheese to the CHEESE STACK or reject it.

 Request<br><br>
GET.VALIDATION [cheese.id] [sequence.no]<br><br>
1. sequence.no: Used to uniquely identify the transaction of corresponding to
the NEW CHEESE.<br><br>
2. cheese.id: Used to uniquely identify the CHEESE. So, the validator can send
validation summary of specified cheese.<br><br>
 Response
[res_code] [validation.summary]<br><br>
3. validation.summary: Member will use this validation.summary to check
the validity of newly created CHEESE.
This is a offline tool, your data stays locally and is not send to any server.