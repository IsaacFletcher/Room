# Understanding Kerberos authentication

****We will need to imagine some applications and services****

###  Client

> - Client application

### Key Distribution Center (KDC)
>- Authentication Service (AS)
>- Ticket Granting Server (TGS)

### Services

>- Service Application to authenticate to

### Administrtion

>- A database to store users and their secrets
>- An application to add new users
>- An application to delete users
---
### Administration

To use Kerberos we need to imagine a database that has client and service principal names with their secret keys

**note: as this is a simple explaination we'll imagine a simple .json file instead of a database**

We'll use bcrypt for deriving the secret key by taking the user's password and adding a salt which is the kdc realm + username.

After that we will write the username, secret, creation timestamp and validity timestamp to the given .json file.

## What Is AS (Authenticaton Service) and How Does It Work?

AS is responsible for issueing the first message that the client will have to decrypt in order to confirm his identity. That message is called TGT (Ticket Granting Ticket)

When the authentication service recieves the first packet after the TCP handshake from the client

which is:

```
username/id : value
service-requested: value
Timestamp: value
Requested lifetime: value (we will remove this one as we don't need the user to decide the lifetime of a ticket)
```

it will look in its database for that user and respond with two messages

First is a message encrypted with the user's secret key,

which contains:

```
TGS Name: value
Timestamp: value
Lifetime for TGT: value
TGS session key: value
```


**note: the principal name of the TGS. example: krbtgt/REALM@REALM. the first realm is the target realm and the second indicates which realm this principal krbtgt/realm belongs to.**

The second message is called TGT (Ticket Granting Ticket) which is encrypted with the TGS's secret key and contains

```
Username/Id: value
TGS Name: value
Timestamp: value
User Ip Addresses
Lifetime for TGT
TGS session key
```

The client decrypts the first message with his hash(password + username@realm) and gets the TGS Session Key.

Then the user generates two messages

First is a plaintext message that contains:

```
Service Principal name: value
Requested Lifetime for the ticket: value
```

The second message is the User Authenticator which is encrypted with the TGS Session key

which contains:

```
Username/ID: value
Timestamp: value
```

These three messages are sent to the TGS and thus the role of the Authentiaction Service is complete:D

**Note: Keep in mind that the AS doesn't pre-authenticate the client before issuing the TGT. This is important to understand AS-REP Roasting attacks**

## TGS

Now we're moving on to the TGS (Ticket Granting Server)

When the TGS recieves the three messages sent by the client, it first looks at the plaintext message

which contains:

```
Service principal name: value
Requested lifetime for TGT: value
```

After that it looks at the service db and checks wether the service actually exists.

If it does, it decrypts the TGT, gets the TGS session key, and decrypts the User Authenticator message.

Once that is complete it starts validating the messages ensuring that the username/ID's are the same the specified IP in the Ticket is the same as the source ip of the packet it recieved and the timestamps (kerberos usualy tolerates up to two minutes difference in timestamps.)

If all that checks out it generates two messages

The first one is encrypted with the TGS session key

which contains:

```
service principal name: value
timestamp: value
service session key: value
```

And the second is called a Service Ticket that is encrypted with the service's secret key

which contains:

```
Username/Id: value
Service principal name: value
timestamp: value
user ip address: value
lifetime for the ticket: value
service session key: value
```

When the client recieves this he decrypts the first message and gets the service session key

Then it generates another User Authentication message which is encrypted with the service session key and contains:

```
Username/ID: value
Timestamp: value
```

The client sends the Service Ticket and the User Authentication messages to the service.

## Service

The service gets the Service Ticket and the User Authentication messages and decrypts the Service Ticket with its secret key, gets the service session key and decrypts the User Authentication message.

It does validation on the messages, and if it's successful it generates a service authentication message which is encrypted by the service session key and contains

```
service principal name: value
timestamp: value
```

and then sends the service authentication message to the client.

the client decrypts the message validates the timestamp and the service principal name, if successful the client and the service have successfully completed the krberos authentication and now have a shared symetric key with which they can communicate securely over an insecure network.

## Some left over questions

>**How are keys generated by the AS and the TGS**

The Authentication Service generates the TGS session key by generating a large totally random number and using that as the TGS session key
example:

```
import os
tgs_session_key = os.urandom(32)
```

The Service session key generated by the TGS works the same way:D

----

## Vulnerabilities: AS-REP Roasting

This vulnerability occures when the AS **doesn't** pre-authenticate the client and issues a TGT.

A mallicious attacker can send a plaintext message to the AS that specifies a diferent user in the username field.

The AS will send a TGT that is encrypted with the specified clients secret key.

The attacker can then attempt to crack the secret key offline, and if successful the attacker can fully compromise that account, as the secret is derived from the users password.


### Mitigation: Policy, Policy, Policy!!!

Windows AD has a pre-auth policy that can be set while setting up Kerberos.

That solves this issue

----
## Vulnerabilities: Kerberoasting

Kerberoasting works similar to AS-REP Roasting.

However in case of Kerberoasting, the attacker has to be authenticated.

The idea of Kerberoasting is to request a Service Ticket from the TGS, with a SPN set to the target service and get a Service Ticket that is encrypted with the service's secret key.

After getting the message, the attacker can attempt to crack it offline, and if successful ultimately compromise a service account.

### Mitigation: Well... Quantum Computers Will Slay the Three Headed Hound

So Microsoft's advisory for the mitigation of this attack is to user complex,long passwords, and use Advanced encryption such as AES-128:D

Also they advise to use Use Group Managed Service Accounts (gMSA) or Delegated Managed Service Accounts (dMSA) wherever possible.

These are essentialy a centralized accounts for various services, so you can manage mny services with just one account.

They advise to use a password with at least 120 characters on these accounts so its harder to crack with a gpu warehouse.

However that still doesn't protect against QC.

You just have to pray that an attacker with access to such technology doesn't target your infrastructure:D
