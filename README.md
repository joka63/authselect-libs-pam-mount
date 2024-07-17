# authselect-libs-pam-mount

This tool aims to add pam_mount support to authselect for Fedora Linux (version 40 or later).

It is designed to behave like Debian's authselect-libs-pam-mount: it not only provides the pam_mount.so module, but it also adds an extended version of the local authselect profile that supports pam_mount without the need to manually edit files in `/etc/pam.d`. 

## Checkout the code

To check out the code from a GitHub git repository to your local machine, run the following command:

```bash
$ git clone https://github.com/joka63/authselect-libs-pam-mount.git
```

## Testing authselect-libs-pam-mount

Before you tryout the tool, checkout the manual pages `man authselect` and its command line help with `sudo authselect --help`. Authselect needs to be run as root so it can perform system-wide changes.

The most important commands are:
```bash
# Show current profile
$ authselect current -r

# List all available profiles
$ sudo authselect list

# See what changes will be done by activating profile named "xlocal" with pam-mount support
$ sudo authselect test xlocal with-silent-lastlog with-mdns4 with-fingerprint with-pam-mount

# Switch from standard profile "local" to "xlocal" with pam-mount support
$ sudo authselect select xlocal with-silent-lastlog with-mdns4 with-fingerprint with-pam-mount
```

