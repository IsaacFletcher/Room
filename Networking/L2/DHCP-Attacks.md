## Intro to DHCP Attacks

To understand these attacks we first need to understand what is the role of DHCP in networks.

DHCP assigns IP addresses hosts that connect to the network, it also assigns the Default Gateway, DNS etc.

A DHCP server has a pool of IP addresses that are availible, every new host gets a lease from that pool.

## DHCP Starvation

We can request all the IP's from the pool by sending 250+ DHCPDISCOVER packets to the DHCP server with 250+ unique MAC addresses.

The DHCP server will give all the availible IP's and won't be able to respond to new legitimate DHCPDISCOVER packets.

## Impact

This can lead to Denial of Service and can make a Rouge DHPC attack more successfull

## Rouge DHCP Attack

We can also start responding to legitimate DHCPDISCOVER packets and impersonate a DHCP server.

As we assign the default gateway and DNS, we can achieve a Man in the Middle attack

## Impact

This can lead to DoS and MITM

## Mitigation

DHCP Snooping is a way of mitigating rouge DHCP server attacks, it sets trusted ports that can send DHCP response packets, others are droped

Also use DHCP option 82, this tracks which port got an IP and doesn't hand out anymore

Also PortSec...duh
