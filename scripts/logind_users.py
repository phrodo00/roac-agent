#!/usr/bin/env python

import dbus, json
bus = dbus.SystemBus()

login1 = bus.get_object('org.freedesktop.login1',
                       '/org/freedesktop/login1')
manager = dbus.Interface(login1, 
                         dbus_interface='org.freedesktop.login1.Manager')
users = [user[1] for user in manager.ListUsers()]
print(json.dumps(users))

