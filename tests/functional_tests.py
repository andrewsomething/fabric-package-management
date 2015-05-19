from fabric.api import settings, task, run
from fabric.operations import local
from fabric.context_managers import cd
from fabric.contrib.files import exists

from fabric_package_management import apt


def docker(cmd):
    return local("docker %s" % cmd, capture=True)


def set_up():
    image_name = 'fab_sshd_ubuntu'
    if image_name not in docker('images'):
        print('Building Docker image...')
        docker('build -t %s .' % image_name)
    else:
        print('Using cached Docker image...')

    container = docker('run -d -p 22 %s' % image_name)
    ssh_port = docker('port %s 22' % container).split(':')[-1]
    host = '127.0.0.1'
    container_host = '%(host)s:%(port)s' % {'host': host, 'port': ssh_port}

    return container, container_host


def tear_down(container):
    print('Destroying Docker container...')
    return docker('kill %s' % container)

    print update.command
    print update.succeeded

def test_apt(container_host):
    print('Running tests for fabric_package_managment.apt')

    update = apt.update()
    assert update.succeeded
    assert update.command == 'apt-get update'

    upgrade = apt.upgrade()
    assert upgrade.succeeded
    assert upgrade.command == 'apt-get upgrade --yes'

    dist_upgrade = apt.dist_upgrade()
    assert dist_upgrade.succeeded
    assert dist_upgrade.command == 'apt-get dist-upgrade --yes'

    update = apt.update(use_sudo=False, verbose=False)
    assert update.succeeded
    assert update.command == 'apt-get update'

    upgrade = apt.upgrade(use_sudo=False, verbose=False)
    assert upgrade.succeeded
    assert upgrade.command == 'apt-get upgrade --yes'

    dist_upgrade = apt.dist_upgrade(use_sudo=False, verbose=False)
    assert dist_upgrade.succeeded
    assert dist_upgrade.command == 'apt-get dist-upgrade --yes'

    install = apt.install(['bpython', 'git'], no_install_recommends=True)
    assert install.succeeded
    assert install.command == 'apt-get install --yes --no-install-recommends  bpython git'
    assert exists('/usr/bin/git')
    assert exists('/usr/bin/bpython')

    install = apt.install('htop', install_suggests=True,
                          use_sudo=False, verbose=False)
    assert install.succeeded
    assert install.command == 'apt-get install --yes  --install-suggests htop'
    assert exists('/usr/bin/htop')

    with cd('/tmp'):
        source = apt.source("python-libcloud", download_only=True)
    assert source.succeeded
    assert source.command == 'apt-get source --download-only python-libcloud'
    assert exists('/tmp/libcloud*dsc')
    assert not exists('/tmp/libcloud*/')

    remove = apt.remove(['bpython', 'git'])
    assert remove.succeeded
    assert remove.command == 'apt-get remove --yes  bpython git'
    assert not exists('/usr/bin/git')
    assert not exists('/usr/bin/bpython')

    remove = apt.remove('htop', purge=True)
    assert remove.succeeded
    assert remove.command == 'apt-get remove --yes --purge htop'
    assert not exists('/usr/bin/htop')
    assert not exists('/usr/lib/python2.7/dist-packages/simplejson/__init__.py')

    build_dep = apt.build_dep('python-libcloud')
    assert build_dep.succeeded
    assert build_dep.command == 'apt-get build-dep --yes python-libcloud'
    assert exists('/usr/lib/python2.7/dist-packages/simplejson/__init__.py')

    autoremove = apt.autoremove()
    assert autoremove.succeeded
    assert autoremove.command == 'apt-get autoremove --yes'

    autoclean = apt.autoclean()
    assert autoclean.succeeded
    assert autoclean.command == 'apt-get autoclean'

    clean = apt.clean()
    assert clean.succeeded
    assert clean.command == 'apt-get clean'
    assert not exists('/var/cache/apt/archives/*deb')

    autoremove = apt.autoremove(use_sudo=False, verbose=False)
    assert autoremove.succeeded
    assert autoremove.command == 'apt-get autoremove --yes'

    autoclean = apt.autoclean(use_sudo=False, verbose=False)
    assert autoclean.succeeded
    assert autoclean.command == 'apt-get autoclean'

    clean = apt.clean(use_sudo=False, verbose=False)
    assert clean.succeeded
    assert clean.command == 'apt-get clean'

    print('All tests for fabric_package_managment.apt succeeded...')


def test():
    container, container_host = set_up()
    try:
        with settings(host_string=container_host,
                      user='root',
                      password='functionaltests'):
            test_apt(container_host)
            print('All tests finished...')
    finally:
        tear_down(container)

if __name__ == '__main__':
    test()
