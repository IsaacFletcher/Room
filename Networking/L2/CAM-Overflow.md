## Intro to CAM

CAM - Content Addressable Memory alsow known as associative memory is a special memory location where MAC + Port pairs are kept for quicker traffic handling.

It works by "remembering" which MAC addresses are connected to which ports based on network traffic.

So for example if a device with MAC address 00:00:00:00:00:01 which is connected to port 1 on the switch does a broadcast request to find out where 00:00:00:00:00:02 device is, the switch will write 00:00:00:00:00:01 - 1 in its CAM table, and when the other device is found it will write that devices MAC address and the port also.

## CAM Overflow

The queston here is, how many pairs can a CAM table contain until its out of space?

The answer is: not that much - about 5000 or so.

So what if we send 100k requests with bogous MAC addresses to the switch?

What will happen to the previousely stored legitimate pairs?

The answer is pretty simple. The CAM table will overflow, push out the legitimate pairs and go into a default state of broadcasting every packet, essentially becoming a network hub.

## Impact

The attacker can now sniff traffic from the whole local network

## Mitigation

Limiting the number of MAC addresses for a single port.

Port security will ensure that in case an attacker connects to a switch and attempts a CAM overflow attack the port will simply lock and not work until an administrator unlocks it.
