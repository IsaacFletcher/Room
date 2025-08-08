## Windows Registry

**Windows registry is the central database both for the Windows operating system and application functionality**

It is structured hierarchically and the fundamental unit of data is called a key, instead of a directory.

Keys can include subkeys or values, each identified by a name,a data type, and content.

To modify the registry, applications open a key by providing its name to an already opened key, leveraging predefined keys that are always accessible.

---

Importand predefined keys:

- **HKEY_CLASSES_ROOT (HKCR)**: Manages file type assosciations and is used by shell and Componend Object Model (COM) applications.

- **HKEY_CURRENT_CONFIG (HKCC)**: Stores hardware configuration details, particularly deviations from default settings.

- **HKEY_CURRENT_USER (HKCU)**: Contains settings for the currently logged-in user, varying between users including the SYSTEM

- **HKEY_LOCAL_MACHINE**: Holds data about the machine, such as hardware and drivers.

- **HKEY_PERFORMANCE_DATA**: Focuses on system performance metrics, with data not stored within the Registry but accessed through specific functions.

- **HKEY_USERS**: Stores default user settings applied to new user accounts.


The Registry organizes data into hives, each representing a groop of keys and their values, associated with specific files that load into memory based on system triggers like boot-up or user login.

---

Here are tha standard hives and their corresponding files:

```
HKEY_CURRENT_CONFIG -> System, System.alt, System.log, System.sav

HKEY_CURRENT_USER -> Ntuser.dat, Ntuser.dat.log

HKEY_LOCAL_MACHINE\SAM -> Sam, Sam.log. Sam.sav

HKEY_LOCAL_MACHINE\Security -> Security, Security.log, Security.sav

HKEY_LOCAL_MACHINE\Software -> Software, Software.log, Software.sav

HKEY_LOCAL_MACHINE\System -> System, System.alt, System.log, System.sav

HKEY_USERS\.DEFAULT -> Default, Default.log, Default.sav
```


To open the Registry GUI Win+R -> regedit will do the job.

To interact with registry from the cmd the **reg** command can be used.

---

The Windows Registry is complex, but crucial component of the operating system, ensuring stability and functionality.

> **A basic understanding of its structure is fundamental for aspiring security professionals**
