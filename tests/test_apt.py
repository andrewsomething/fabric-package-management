import unittest
import os

from fabric.api import settings
from fabric.operations import local
from fabric.context_managers import cd
from fabric.contrib.files import exists

from fabric_package_management import apt


def docker(cmd):
    return local("docker %s" % cmd, capture=True)


class AptTest(unittest.TestCase):
    """
    These tests are run against a local Docker container that is treated
    like a remote host. The Docker image is built from the Dockerfile in this
    directory which simply provides a SSH server.
    """
    def setUp(self):
        image_name = 'fab_sshd_ubuntu'
        if image_name not in docker('images'):
            print('Building Docker image...')
            dfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 'Dockerfile.apt')
            docker('build -t %s -f %s .' % (image_name, dfile))
        else:
            print('Using cached Docker image...')

        self.container = docker('run -d -p 22 %s' % image_name)
        self.ssh_port = docker('port %s 22' % self.container).split(':')[-1]
        self.host = '127.0.0.1'
        self.container_host = '%(host)s:%(port)s' % {'host': self.host,
                                                     'port': self.ssh_port}

    def tearDown(self):
        print('Destroying Docker container...')
        return docker('rm -f %s' % self.container)

    def test_update(self):

        test_source = 'trusty-backports'
        test_update_command = "apt-get update -o Dir::Etc::sourceparts='-' "
        test_update_command += "-o Dir::Etc::sourcelist='sources.list.d/{}.list'".format(test_source)

        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):

            update = apt.update()
            self.assertTrue(update.succeeded)
            self.assertEqual(update.command, 'apt-get update')

            update = apt.update(use_sudo=False, verbose=False)
            self.assertTrue(update.succeeded)
            self.assertEqual(update.command, 'apt-get update')

            update = apt.update(source_name=test_source)
            self.assertTrue(update.succeeded)
            self.assertEqual(update.command, test_update_command)

    def test_upgrade(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):

            upgrade = apt.upgrade()
            self.assertTrue(upgrade.succeeded)
            self.assertEqual(upgrade.command, 'apt-get upgrade --yes')

            upgrade = apt.upgrade(use_sudo=False, verbose=False)
            self.assertTrue(upgrade.succeeded)
            self.assertTrue(upgrade.command, 'apt-get upgrade --yes')

    def test_dist_upgrade(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):
            dist_upgrade = apt.dist_upgrade()
            self.assertTrue(dist_upgrade.succeeded)
            self.assertEqual(dist_upgrade.command,
                             'apt-get dist-upgrade --yes')

            dist_upgrade = apt.dist_upgrade(use_sudo=False, verbose=False)
            self.assertTrue(dist_upgrade.succeeded)
            self.assertEqual(dist_upgrade.command,
                             'apt-get dist-upgrade --yes')

    def test_install(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):

            install = apt.install(['bpython', 'git'],
                                  no_install_recommends=True)
            self.assertTrue(install.succeeded)
            expt = 'apt-get install --yes --no-install-recommends bpython git'
            self.assertEqual(install.command, expt)
            self.assertTrue(exists('/usr/bin/git'))
            self.assertTrue(exists('/usr/bin/bpython'))

            install = apt.install('htop', install_suggests=True,
                                  use_sudo=False, verbose=False)
            self.assertTrue(install.succeeded)
            expt = 'apt-get install --yes --install-suggests htop'
            self.assertEqual(install.command, expt)
            self.assertTrue(exists('/usr/bin/htop'))

    def test_source(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):

            with cd('/tmp'):
                source = apt.source("python-libcloud", download_only=True)
            self.assertTrue(source.succeeded)
            self.assertEqual(source.command,
                             'apt-get source --download-only python-libcloud')
            self.assertTrue(exists('/tmp/libcloud*dsc'))
            self.assertFalse(exists('/tmp/libcloud*/'))

    def test_remove(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):

            remove = apt.remove(['bpython', 'git'])
            self.assertTrue(remove.succeeded)
            self.assertEqual(remove.command,
                             'apt-get remove --yes  bpython git')
            self.assertFalse(exists('/usr/bin/git'))
            self.assertFalse(exists('/usr/bin/bpython'))

            remove = apt.remove('htop', purge=True)
            self.assertTrue(remove.succeeded)
            self.assertEqual(remove.command,
                             'apt-get remove --yes --purge htop')
            htop = exists('/usr/bin/htop')
            self.assertFalse(htop)
            json = exists(
                '/usr/lib/python2.7/dist-packages/simplejson/__init__.py')
            self.assertFalse(json)

    def test_build_dep(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):

            build_dep = apt.build_dep('python-libcloud')
            self.assertTrue(build_dep.succeeded)
            self.assertEqual(build_dep.command,
                             'apt-get build-dep --yes python-libcloud')
            json = exists(
                '/usr/lib/python2.7/dist-packages/simplejson/__init__.py')
            self.assertTrue(json)

    def test_autoremove(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):

            autoremove = apt.autoremove()
            self.assertTrue(autoremove.succeeded)
            self.assertEqual(autoremove.command, 'apt-get autoremove --yes')

            autoremove = apt.autoremove(use_sudo=False, verbose=False)
            self.assertTrue(autoremove.succeeded)
            self.assertEqual(autoremove.command, 'apt-get autoremove --yes')

    def test_autoclean(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):

            autoclean = apt.autoclean()
            self.assertTrue(autoclean.succeeded)
            self.assertEqual(autoclean.command, 'apt-get autoclean')

            autoclean = apt.autoclean(use_sudo=False, verbose=False)
            self.assertTrue(autoclean.succeeded)
            self.assertEqual(autoclean.command, 'apt-get autoclean')

    def test_clean(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):

            clean = apt.clean()
            self.assertTrue(clean.succeeded)
            self.assertEqual(clean.command, 'apt-get clean')
            self.assertFalse(exists('/var/cache/apt/archives/*deb'))

            clean = apt.clean(use_sudo=False, verbose=False)
            self.assertTrue(clean.succeeded)
            self.assertEqual(clean.command, 'apt-get clean')

    def test_installed(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):

            self.assertFalse(apt.installed('rolldice'))
            apt.install('rolldice')
            self.assertTrue(apt.installed('rolldice'))

    def test_check_version_available(self):
        with settings(host_string=self.container_host,
                      user='root',
                      password='functionaltests'):
            self.assertTrue(apt.check_version_available(package='apache2', version='2.4.7-1ubuntu4'))
            self.assertFalse(apt.check_version_available(package='apache2', version='1.0'))
