Installing on Centos
====================

In this directory there the files to install a roac daemon on the system.

Just copy the files in this directory like this:

=========================== ==============
File                        Destination
=========================== ==============
roacd                       /etc/sysconfig
roacd.conf, roacd_root.conf /etc/init
roac.cfg                    /etc
=========================== ==============

Then you have to chose whether you want to run roacd as a regular user  or as
root. We strongly recommend to run it as a user, but some scripts might need
to run as root (none of the included scripts do, anyhow, you can use some
cleverness with uid, sudo -n and paswordless sudo to make scripts gain whatever
permissions they need).

To run it as a user, simply create a user to run roacd and especify its name
in /etc/sysconfig/roacd, then uncomment the start line on /etc/init/roacd.conf.

To run as root, uncomment the start line on roacd_root.conf

You might also want to copy the example scripts to some location in the system
and list it in /etc/roac.conf. The default location is /var/lib/roac/scripts.
