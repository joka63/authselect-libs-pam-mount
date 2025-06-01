# authselect-libs-pam-mount

This tool aims to add pam_mount support to authselect for Fedora Linux (version 41 or later).

It provides 3 files that have to be changed in the local's authselect profile to support pam_mount.

## Installation on Fedora Workstation
```bash
sudo dnf copr enable joka63/extras
sudo dnf install authselect-libs-pam-mount
```

## Installation on Fedora Atomic Desktop
```bash
sudo curl -o /etc/yum.repos.d/_copr:copr.fedorainfracloud.org:joka63:extras.repo https://copr.fedorainfracloud.org/coprs/joka63/extras/repo/fedora-42/joka63-extras-fedora-42.repo
sudo rpm-ostree install authselect-libs-pam-mount
```
On Fedora Atomic Desktop you need to reboot. 
## Manual install
Create a copy of your local authselect profile:
```bash
authselect create-profile xlocal --base-on local
```
This creates a new folder `/etc/authselect/custom/xlocal`, containing a copy of the local profile.
Then download the 3 files in `profiles/xlocal` from this repo and copy them to `/etc/authselect/custom/xlocal`, e.g.:
```bash
wget https://github.com/joka63/authselect-libs-pam-mount/archive/refs/heads/master.zip
unzip -j master.zip '*/profiles/xlocal/*' -d /etc/authselect/custom/xlocal
```

## Testing authselect-libs-pam-mount

**Note:** After installation as package the new profile has the name `xlocal`. If you have created it manually it's name is `custom/xlocal`. 

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
## Activating the extended authselect profile
The new authselect profile `xlocal` will not be selected automatically during installation of the authselect-lib-pam-mount package. 

If your current profile is `local` you can enter the following command:
```bash
authselect select x$(authselect current -r) with-pam-mount
```
or explicitly:
```
authselect select xlocal with-silent-lastlog with-mdns4 with-fingerprint with-pam-mount
```
This selects the new profile "xlocal" with all features previously enabled for profile "local" and the feature "with-pam-mount" which adds support for pam_mount. 

## Use Case: LUKS Encrypted Home Directory on Fedora

### Preliminaries

* Setup a Fedora Silverblue or Workstation OS. The Fedora installer normally creates 3 partitions (EFI, boot and sysroot).
* Create a partition at `/dev/nvme0n1p4` (or `/dev/vda4` in a virtual machine) with the intention that it would be mounted at `/var/home/privat`. The 4th partition should contain a LUKS encrypted file system.
* Add a new user account `privat` (if not yet done). It should have the same password as the LUKS partition!
* Install the package `authselect-libs-pam-mount` as described above.

### Actions
All following commands should called in a sudo or root shell:

* Activate authselect profile `xlocal`:
```bash
authselect select xlocal with-silent-lastlog with-mdns4 with-fingerprint with-pam-mount
```
* Prepare the encrypted home directory:
```
mount.crypt /dev/vda4 /var/home/privat
chown -R privat:privat /var/home/privat
restorecon -R /var/home/privat
umount.crypt /var/home/privat
```
This ensures that the user `privat` has write access to its home directory after mounting. The command `mount.crypt` is part of the pam_mount package.
* Add the following line to file `/etc/security/pam_mount.conf.xml`, assuming it's a BTRFs file system. (Adapt `options` and `fstpye` if you use another file system for your home directory partition):
```
<volume user="privat" mountpoint="/var/home/privat" path="/dev/vda4" fstype="crypt" options="noatime,compress=zstd:1" />
```
See the man page of `pam_mount.conf` for additional options. You may wish to change the password prompt or make sure that the home directory gets unmounted when you logout.
