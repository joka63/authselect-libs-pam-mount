# LibPAM-Mount

It is designed to behave like Debian's libpam-mount: it not only provides the pam_mount.so module, but also adds it an extended version of the local authselect profile. 

This tool aims to add pam_mount support to authselect.

## Checkout the code

To check out the code from a GitHub git repository to your local machine, run the following command:

```bash
$ git clone https://github.com/joka63/libpam-mount.git
```

## Testing libpam-mount

Before you tryout the tool, checkout its manual pages `man authselect` and its command line help with `sudo authselect --help`. Authselect needs to be run as root so it can perform system-wide changes.

The most important commands are:

```bash
# List all available profiles
$ sudo authselect list

# See what changes will be done by activating profile named $profilename
$ sudo authselect test $profilename

# Activate a profile named $profilename on the system
$ sudo authselect select $profilename
```

