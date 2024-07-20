# authselect-libs-pam-mount

This tool aims to add pam_mount support to authselect for Fedora Linux (version 40 or later).

It provides 3 files that have to be changed in the local's authselect profile to support pam_mount. 

## Manual install
Create a copy of your local authselect profile:
```
authselect create-profile xlocal --base-on local
```
This creates a new folder `/etc/authselect/custom/xlocal`, containing a copy of the local profile.
Then download the 3 files in `profiles/xlocal` from this repo and copy them to `/etc/authselect/custom/xlocal`, e.g.:
```
wget https://github.com/joka63/authselect-libs-pam-mount/archive/refs/heads/master.zip
unzip -j master.zip '*/profiles/xlocal/*' -d /etc/authselect/custom/xlocal
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

