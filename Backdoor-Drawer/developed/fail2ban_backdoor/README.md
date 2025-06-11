# Developing a Fail2Ban Linux Backdoor

While looking into the topic of persistance i got an idea.

The idea is to basicaly create or overwrite an existing Fail2Ban configuration on the victim host, that will work as intended, but when certain conditions are met, provide a reverse shell or add a ssh public key to the authorized_hosts ultimately giving the attacker a backdoor that can be opened/closed at any moment by the attacker.

### Prerequisites

- Understand how Fail2Ban works and how to configure a custom action
- Implement Fail2Ban with shell script
- Obfuscate and integrate the backdoor
- (optional) Develop a script that will exploit the backdoor and establish a reverse/ssh connection with the victim host

## Step 1: Understanding How Fail2Ban Works

In its essense Fail2Ban is an application that monitors the failed login attempts and bans an IP address based on a predefined quota for failed attempts.

It has the capability to block temporarily and permanently

Fail2Ban is set up with a configuration file which is located in /etc/fail2ban/jail.local in Linux

Fail2Ban example configuration:

```
[Default]

bantime = 10m
port = 22
destmail = root@localhost
sender = root@
mta = sendmail
banaction = iptables-multiport
banaction_allports = iptables-allports
```

The banaction is configured separately, the file is located at /etc/fail2ban/action.d/iptables-multiport.conf

With comments removed the file looks like this

```
[INCLUDES]
before = iptables-blocktype.conf

[Definition]
actionstart = iptables -N fail2ban-<name>
                iptables -A fail2ban-<name> -j RETURN
                iptables -I <chain> -p <protocol> -m multiport --dports <port> -j fail2ban-<name>

actionstop = iptables -D <chain> -p <protocol> -m multiport --dports <port> -j fail2ban-<name>

actioncheck = iptables -n -L <chain> | grep -a 'fail2ban-<name>[ \t]'

actionban = iptables -I fail2ban-<name> 1 -s <ip> -j <blocktype>

actionunban = iptables -D fail2ban-<name> -s <ip> -j <blocktype>

[Init]
name = default
port = ssh
protocol = tcp
chain = INPUT
```

First it sources iptables-blocktype.conf which defines the blocktype parameter. It is the configuration of what restriction will be set to a banned client
