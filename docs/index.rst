.. fabric-package-management documentation master file, created by
   sphinx-quickstart on Sat Aug 29 19:39:43 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

fabric-package-management
=========================

As the name implies, fabric-package-management is a collection of
Fabric_ tasks for package management.

Code Documentaion:
------------------

.. toctree::
   :maxdepth: 4

   fabric_package_management

.. automodule:: fabric_package_management
    :members:
    :undoc-members:
    :show-inheritance:

Example
-------

.. code-block:: python

    #!/usr/bin/python

    from fabric.api import task, prompt, env
    from fabric.context_managers import cd
    from fabric.operations import reboot

    from fabric_package_management import apt

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Fabric: http://www.fabfile.org/