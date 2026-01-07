# HTTP Request Smuggling

HTTP Request Smuggling is a technique of desyncronizing the back-end and the front-end servers of an application.

## What does this even mean?

So suppose we have a front-end reverse proxy and a back-end server that responds to our requests.

The front-end proxy can restrict our access to certain resources. However if we desyncronize those two servers we would be able to get to the back-end server directly so to say, without front-end filtering.

This could also allow us to do cache poisoning, DoS and much more.

## The technical "How?" and prerequisits

The vulnerability arises from the HTTP specification itself, or exactly HTTP 1.1 specification.

In the specification there are no clear boundaries between when a HTTP request ends and where the other one begins.

In the HTTP 1.1 specification there are two ways an HTTP server knows where a HTTP request ends:

- The `Content-Length` header
- The `Transfer-Encoding` header

You are probably familiar with the `Content-Length` header as it is more commonly used and seen when dealing with traditional requests. The `Transfer-Encoding` header is used for specifying the HTTP request/response encoding between communicating nodes (gzip, deflate, compress, chunked) and is used when the total size of the response/request isn't known beforehand.

**So what happens if we make a request that contains both these headers?**

In the HTTP 1.1 specification it is stated that if both of these headers are present the `Content-Length` header should be ignored.

This solves a number of conflicting scenarios. However, it does not eliminate them completely.

If two servers are in play they might support different headers, or process malformed headers differently. 

**This gives us the opportunity to desyncronize them!**

## Types of HTTP Request Smuggling

These types refer to scenarios where 2 servers are in play (front and back-end)

### CL:TE

This type of desyncronization arises when the front-end server doesn't support `Transfer-Encoding` while the back-end does.

An example of CL:TE desyncronization attack goes like this:

```
POST / HTTP/1.1
Host: vulnerablesite.com
User-Agent: attacker
Content-Length: <automatic>
Transfer-Encoding: chunked

0

G
```

So what this does is, the request goes to the front-end server which looks at the `Content-Length` header and proxies the request to the back-end server. The back-end server ignores the `Content-Length` header and treats the `G` as a start to a different HTTP request, which causes the next HTTP request to look like this:

```
GPOST / HTTP/1.1
...
```

The `0` in the request tells the back-end HTTP server that there are 0 bytes incoming (basically terminates the connection).

### Exploitation with CL:TE

There are many possible exploits for this vulnerability.

**Scenario N1:**

If the restriction to access `/admin` is configured on the front-end server, we can bypass this restriction with this desyncronization method.

```
POST / HTTP/1.1
Host: vulnerablesite.com
User-Agent: attacker
Content-Length: <automatic>
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: localhost
Content-Length: n
Content-Type: application/json

x=
```

When the second request gets directly to the back-end server we are able to access `/admin`, the `x` parameter in the request is to "neutrulize" the next request's headers. If we don't add that, the headers will conflict with eachother and cause an error.


### TE:CL 


