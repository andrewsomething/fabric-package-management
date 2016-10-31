from fabric.api import hide, run, settings, sudo
from fabric.context_managers import shell_env
from fabric.contrib.files import exists


def _run_cmd(func, cmd, verbose):
    """
    Utility function to run commands respecting `use_sudo` and `verbose`.
    """
    with shell_env(REDHAT_FRONTEND='noninteractive'):
        if verbose:
            return func(cmd)
        with settings(hide('everything')):
            return func(cmd)


def install(packages, assume_yes=True, 
            use_sudo=True, verbose=True):
    """
    Install packages on the remote host via Yum.

    Args:
      packages (list or str): The packages to install.
      no_install_recommends (bool): Yum will not consider recommended packages
        as a dependencies for installing. (Default: `True`)
      install_suggests (bool): Yum will consider suggested packages as a
        dependency for installing. (Default: `False`)
      assume_yes (bool): If `True`, Yum will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    if not isinstance(packages, str):
        packages = ' '.join(packages)

    if assume_yes:
        yes = '--assumeyes'
    else:
        yes = ''

    func = use_sudo and sudo or run
    cmd = 'yum {0} install {1} {2} {3}'.format(yes, packages)

    return _run_cmd(func, cmd, verbose)


def update(use_sudo=True, verbose=True):
    """
    Update Yum's package index files on the remote host.

    Args:
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    func = use_sudo and sudo or run
    cmd = 'yum makecache'

    return _run_cmd(func, cmd, verbose)


def upgrade(assume_yes=True, use_sudo=True, verbose=True):
    """
    Install the newest versions of all packages on the remote host.

    Args:
      assume_yes (bool): If `True`, Yum will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    if assume_yes:
        yes = '--assumeyes'
    else:
        yes = ''

    func = use_sudo and sudo or run
    cmd = 'yum {0} upgrade'.format(yes)

    return _run_cmd(func, cmd, verbose)


def dist_upgrade(use_sudo=True, verbose=True):
    """
    Same as `upgrade`, but Yum will attempt to intelligently handle changing
    dependencies, installing new dependencies as needed.

    Args:
      assume_yes (bool): If `True`, Yum will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """

    func = use_sudo and sudo or run
    cmd = 'yum distro-sync'

    return _run_cmd(func, cmd, verbose)


def remove(packages, purge=False, assume_yes=True, use_sudo=True,
           verbose=True):
    """
    Remove a package or list of packages from the remote host.

    Args:
      packages (list or str): The packages to install.
      purge (bool): If `True` any configuration files are deleted too.
        (Default: `False`)
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    if not isinstance(packages, str):
        packages = ' '.join(packages)

    if assume_yes:
        yes = '--assumeyes'
    else:
        yes = ''

    if purge:
        purge = '--purge'
    else:
        purge = ''

    func = use_sudo and sudo or run
    cmd = 'yum {0} remove {1} {2}'.format(yes, purge, packages)

    return _run_cmd(func, cmd, verbose)


def clean(use_sudo=True, verbose=True):
    """
    Clears out retrieved package files.

    Args:
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
       (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    func = use_sudo and sudo or run
    cmd = 'yum clean all'

    return _run_cmd(func, cmd, verbose)


def autoclean(use_sudo=True, verbose=True):
    """
    Like `clean`, but only removes package files that can no longer
    be downloaded.

    Args:
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    func = use_sudo and sudo or run
    cmd = 'yum autoclean'

    return _run_cmd(func, cmd, verbose)


def autoremove(assume_yes=True, use_sudo=True, verbose=True):
    """

    Args:
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """

    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    func = use_sudo and sudo or run
    cmd = 'yum autoremove {0}'.format(yes)

    return _run_cmd(func, cmd, verbose)


def installed(package, use_sudo=True):
    """
    Check if a package is installed on the system.

    Returns `True` if installed, `False` if it is not.

    Args:
      package (str): The package to check if installed.
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `False`)
    """
    func = use_sudo and sudo or run
    cmd = "rpm -q {0}".format(packagfe)
    with settings(warn_only=True):
        installed = _run_cmd(func, cmd, verbose=False)
    if installed.find("install ok installed") > -1:
        return True
    return False
