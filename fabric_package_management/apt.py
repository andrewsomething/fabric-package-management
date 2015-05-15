from fabric.api import sudo
from fabric.context_managers import shell_env
from fabric.contrib.files import exists


def install(packages, assume_yes=True, no_install_recommends=False,
            install_suggests=False):
    """
    Install packages on the remote host via Apt.

    Args:
      packages (list or str): The packages to install.
      no_install_recommends (bool):
      install_suggests (bool):
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
    """
    if not isinstance(packages, str):
        packages = ' '.join(packages)

    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    if no_install_recommends:
        recommends = '--no-install-recommends'
    else:
        recommends = ''

    if install_suggests:
        suggests = '--install-suggests'
    else:
        suggests = ''

    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        sudo('apt-get install {0} {1} {2} {3}'.format(yes,
                                                      recommends,
                                                      suggests,
                                                      packages))


def update():
    """
    Update Apt's package index files on the remote host.
    """
    sudo('apt-get update')


def upgrade(assume_yes=True):
    """
    Install the newest versions of all packages on the remote host.

    Args:
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
    """
    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    sudo('apt-get upgrade {0}'.format(yes))


def dist_upgrade(assume_yes=True):
    """
    Same as `upgrade`, but Apt will attempt to intelligently handle changing
    dependencies, installing new dependencies as needed.

    Args:
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
    """
    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    sudo('apt-get dist-upgrade {0}'.format(yes))


def remove(packages, purge=False, assume_yes=True):
    """
    Remove a package or list of packages from the remote host.

    Args:
      packages (list or str): The packages to install.
      purge (bool): If `True` any configuration files are deleted too.
        (Default: `False`)
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
    """
    if not isinstance(packages, str):
        packages = ' '.join(packages)

    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    if purge:
        purge = '--purge'
    else:
        purge = ''

    sudo('apt-get remove {0} {1} {2}'.format(yes, purge, packages))


def clean():
    """
    Clears out retrieved package files.
    """
    sudo('apt-get clean')


def autoclean():
    """
    Like `clean`, but only removes package files that can no longer
    be downloaded.
    """
    sudo('apt-get clean')


def autoremove(assume_yes=True):
    """

    Args:
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
    """

    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    sudo('apt-get autoremove {0}'.format(yes))


def source(package, download_only=False):
    """
    Download a given source package.

    Args:
      package (str): The source package to download.
      download_only (bool): If `True`, the source package will not be
        unpacked. (Default: `False`)
    """

    if download_only:
        download = '--download-only'
    else:
        download = ''

    sudo('apt-get source {0} {1}'.format(download, package))


def build_dep(package, assume_yes=True):
    """
    Install the build dependencies for a given source package.

    Args:
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
    """

    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    sudo('apt-get build-dep {0} {1}'.format(yes, package))


def reboot_required():
    """
    Check if a reboot is required after intalling updates.

    Returns:
      bool: `True` if a reboot is required, `False` if not.
    """
    return exists('/var/run/reboot-required')
