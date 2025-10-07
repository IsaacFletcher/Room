## Web Application Reconnaissance

In the area of web application recon Project Discovery has a lot of usefull tools.

I'll try to cover as much as possible by using a real target as an example and try to earn some money while doing it:D

**So grab a coffee or a vodka and enjoy my desperate attempts to buy my gf a better meal next week**

### Installation

To get all the tools that I'm going to be covering here follow these steps.

(My host OS is Arch linux, so keep that in mind if something's not working.)

1. Install golang

```bash
sudo pacman -Syyu
sudo pacman -S go
```

2. Install PDTM (Project Discovery Tool Manager)

```bash
go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest
```

This will install the pdtm and from here you can easily install all the tools and also update them.

```bash
pdtm -ia
```

To update pdtm just do

```bash
pdtm -up
```

Also you need to install massdns for the shuffledns tool to work.

```bash
git clone https://github.com/blechschmidt/massdns.git
cd massdns
make
sudo cp ./bin/massdns /usr/bin/
```

Nice! Now you should be all set up.

### Methodology

So it's really easy to just run tools and see output. However we need to have a clear understanding of what we're doing.

**Understanding is key to understanding**

What are we trying to achieve here?

We want to have as much information about the assets of the target as possible.
After that we want to know as much information about the contents of said assets of the target as possible.

Why? This will give us as large attack vector as possible.
More attack vectors, bigger chance of getting a better meal:D

There is never too much recon.

### Asset Discovery

Okay lets start with asset discovery.

First thing we look for in a target is the domain and subdomais.
There are a lot of ways to enumerate subdomains.
The first thing that pops in my head is using **subfinder**.
To use subfinder efficiently go to the providers configuration and add API keys.

After that you will get resaults with just

```bash
subfinder -d arubanetworks.com -all
```
(Good practice to pipe the output to tee and save the output for later use.)

#### Shuffledns

Another method for enumerating subdomains is by bruteforcing your way with Shuffledns.

You should have a list of resolvers and a wordlist to bruteforce subdomains.

Resolvers: https://raw.githubusercontent.com/trickest/resolvers/refs/heads/main/resolvers.txt

Wordlist: https://wordlists-cdn.assetnote.io/data/automated/httparchive_subdomains_2025_09_27.txt

These are just some good wordlists, don't limit yourself to only one pair of wordlists

Now we can bruteforce some subdomains.

```bash
shuffledns -d arubanetworks.com -w wordlist.txt -r resolvers.txt -mode bruteforce
```

Use -silent for only the domains as the output (usefull if you pipe the output to another tool)
This will bruteforce with DNS and give you a list of domains that resolved to an IP address.

#### Finding permutations with alterx

After finding some amount of subdomains you can see if there are any permutations of that subdomains.
There's a tool for that!

Alterx will take a list of domains and alter the subdomain and give you a list.
Just pipe the domains from shuffledns to alterx and get a new list of subdomains.

Pipe that into another file for later use.

```bash
echo 'something.example.com' | alterx | tee alterx-subdomains.txt
```

#### Checking for availability with dnsx

After getting the alterx-subdomains you can check if they exist with dnsx.
Just pipe the output to dnsx.

```bash
cat alterx-subdomains.txt | dnsx
```

This will give you the ones that are available.

#### Fast port scanning with naabu

After getting a decent amount of subdomains we can look for open ports.
Usually you would use something like rustscan or nmap for that, but projectdiscovery tools work really harmonicaly together.

Just pipe the output to naabu with some arguments and it will get the job done.

```bash
cat domains.txt | alterx | dnsx | naabu -top-ports 100 -ep 22 # (Exclude port 22)
```

### Content Discovery

Next up is content discovery.

After enumerating all these assets we now can proceed to the messy part.
There is a lot more content than assets. We need to filter the irrelevant or non interesting content as much as possible.

#### Content Availability with httpx

httpx is a great tool for automated availability checking.
There are a lot of usefull parameters but you can check those for yourself.

Some basic parameters allow us to get the title, content type, content length, and many others in a compact way.

```bash
cat domains.txt | alterx | dnsx | naabu -top-ports 100 -ep 22 | httpx -title -sc -cl -location -fr # Show title, status-code, content-length, location header, follow redirects
```

This is a high level overview of httpx and it has a lot more functionality (read the documentation)

#### Crawling with katana

After discovering all this content we want to also automate the crawling process. Katana does that in a fucking awesome way.

Basic usage of katana is with just giving the url.

```bash
katana -u http://example.com
```

But this will not give much resaults.

The cool thing about katana is that it can crawl javascript files and get endpoints from there as well.

```bash
katana -u http://example.com -xhr -jsl -aff # Look in DOM, javascript file crawling, automatically fill forms and see if there are any endpoints
```

You can also give custom headers to katana with -H (can be used for session, user-agent etc.).


### Actual Workflow

Okay so we got some idea on how to use these tools.

Now we need to chain them all together and form a automated workflow.

An example workflow would be like this.

```bash
subdfinder -d example.com -all -silent | alterx -silent | dnsx -silent | naabu -top-ports 100 -silent | tee recon.txt
```

Or something like

```bash
shuffledns -d example.com -w wordlist.txt -r resolvers.txt -mode bruteforce -silent | alterx -silent | dnsx -silent | naabu -top-ports 100 -silent | httpx -title -sc -cl -location -fr | tee recon.txt
```

Variations are endless. Adapt to your own needs and have fun.
