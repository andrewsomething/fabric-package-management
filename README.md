# fabric-package-management

As the name implies, fabric-package-management is a collection of [Fabric](http://www.fabfile.org/)
tasks for package management. There's nothing too fancy going on here. It's aim is to simply not
have to copy and paste similar convenience functions into many a Fabfile.

[![Build Status](https://travis-ci.org/andrewsomething/fabric-package-management.svg?branch=master)](https://travis-ci.org/andrewsomething/fabric-package-management)

## Example:

```py
#!/usr/bin/python

from fabric.api import task, prompt, env
from fabric.context_managers import cd
from fabric.operations import reboot

from fabric_package_managment import apt

@task()
def run():
    apt.update()
    apt.upgrade()
    apt.install(['bpython', 'git'])
    with cd('/tmp'):
        apt.source("python-libcloud", download_only=True)
    apt.remove('bpython', purge=True)
    apt.autoremove()
    apt.autoclean()
    if apt.reboot_required():
        prompt("Reboot required. Initiate now?\nYes/No?",
            "response",
            default="No",
            validate=r'yes|Yes|YES|no|No|NO')
        if env.response.lower() == "yes":
            reboot()
```
