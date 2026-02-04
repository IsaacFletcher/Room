# Windows Local Logon Process 

After boot the first usermode process is **smss.exe** (Session Manager Sub-System)

It's job is to create sessions.

Initialy it creates two sessions

## Session 0: Operating System

### Child Processes

- **csrss.exe**
- **wininit.exe**

#### CSRSS.EXE (Client Server Runtime Sub-System)

It's job is to manage processes and threads

When a usermode process calls a function for process/thread creation - win32 libraries send an IPC (inter process call) to csrss.exe which does the actual work without compromising the kernel. 
> [!IMPORTANT]
> Only two instances of csrss.exe should be present in a given task manager.

#### WININIT.EXE (Windows Initialization Process)

It's job is to start 
- services.exe 
- lsass.exe 
- lsm.exe

**We'll cover lsass.exe here, because this is about windows logon.**

#### LSASS.EXE (Local Security Authority Subsystem Service)

It validates the local account credentials
Generates security tokens for account sessions 
Manages security policies and settings

## Session 1: User Side

### Child Processes 

- **csrss.exe**
- **winlogon.exe**

> [!IMPORTANT]
> Only one instance of smss.exe can be present at ANY given time.

