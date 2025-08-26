## The Beast We Call DNS

Domain Name System (DNS) is a L7 protocol that translates human-readable domain names into IP addresses.

### What?

When a computer is trying to access a website (example.com) it can't just write destination website -> example.com and send a packet. In a tcp/udp packet the src.ip and dst.ip feilds are necessary for a protocol above L2. So to access a website it first has to know what IP address is behind example.com.

This is where DNS comes kicking down doors.

### How?

In order to understand how our example.com converts into an IP address, we must know about the 4 servers that are doing the heavy lifting.

- **DNS Recursor**
- **Root Nameserver**
- **TLD Nameserver**
- **Authorative Nameserver**


#### DNS Recursor: The Librarian

The Librarian is the one that is asked the initial question of where is example.com.

It is then responsible for satisfying the clients query by making additional queries to other servers.

If the Librarian doesn't have a cache of the example.com it will start making queries to the other servers, which can be imagined as sections in the book rack, shelf and collection.

The first query that the Librarian makes is to the root nameserver

#### DNS Root Nameserver: The Book Rack

Upon getting a query from the Librarian the Book Rack sees if it has the domain name cached.

If not, it makes a query to the TLD (Top Level Domain) Server.

To understand this concept better, we need to know about "zones". The administration of the DNS is structured in a hirarchycal way, using different managed areas.

So for example root nameserver A is responsible for querying TLD nameservers .ORG .COM .NET and root nameserver B is responsible for .IN .BZ etc.

![Alt text](dns-root-server.png)
