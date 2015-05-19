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


def test_apt(container_host):
    print('Running tests for fabric_package_managment.apt')
    apt.update()
    apt.upgrade()
    apt.dist_upgrade()
    apt.install(['bpython', 'git'])
    assert exists('/usr/bin/git')
    assert exists('/usr/bin/bpython')
    apt.install('htop')
    assert ('/usr/bin/htop')
    with cd('/tmp'):
        apt.source("python-libcloud", download_only=True)
    assert exists('/tmp/libcloud*dsc')
    assert not exists('/tmp/libcloud*/')
    apt.remove(['bpython', 'git'])
    assert not exists('/usr/bin/git')
    assert not exists('/usr/bin/bpython')
    apt.remove('htop', purge=True)
    assert not exists('/usr/bin/htop')
    assert not exists('/usr/lib/python2.7/dist-packages/simplejson/__init__.py')
    apt.build_dep('python-libcloud')
    assert exists('/usr/lib/python2.7/dist-packages/simplejson/__init__.py')
    apt.autoremove()
    apt.autoclean()
    apt.clean()
    assert not exists('/var/cache/apt/archives/*deb')
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
