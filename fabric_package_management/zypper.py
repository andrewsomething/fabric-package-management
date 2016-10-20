from fabric.api import hide, run, settings, sudo
from fabric.context_managers import shell_env
from fabric.contrib.files import exists


def _run_cmd(func, cmd, verbose):
    """
    Utility function to run commands respecting `use_sudo` and `verbose`.
    """
    with shell_env(SUSE_FRONTEND='noninteractive'):
        if verbose:
            return func(cmd)
        with settings(hide('everything')):
            return func(cmd)


def install(packages, assume_yes=True, no_install_recommends=False,
            use_sudo=True, verbose=True):
    """
    Install packages on the remote host via Zypper.

    Args:
      packages (list or str): The packages to install.
      no_install_recommends (bool): Zypper will not consider recommended packages
        as a dependencies for installing. (Default: `True`)
      assume_yes (bool): If `True`, Zypper will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    if not isinstance(packages, str):
        packages = ' '.join(packages)

    if assume_yes:
        yes = '-y'
    else:
        yes = ''

    if no_install_recommends:
        recommends = '--no-recommends'
    else:
        recommends = ''

    func = use_sudo and sudo or run
    cmd = 'zypper install {0} {1} {2} {3}'.format(yes,
                                                   recommends,
                                                   packages)

    return _run_cmd(func, cmd, verbose)


def update(use_sudo=True, verbose=True):
    """
    Update Zypper's package index files on the remote host.

    Args:
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    func = use_sudo and sudo or run
    cmd = 'zypper refresh'

    return _run_cmd(func, cmd, verbose)


def upgrade(assume_yes=True, use_sudo=True, verbose=True):
    """
    Install the newest versions of all packages on the remote host.

    Args:
      assume_yes (bool): If `True`, Zypper will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    if assume_yes:
        yes = '-y'
    else:
        yes = ''

    func = use_sudo and sudo or run
    cmd = 'zypper update {0}'.format(yes)

    return _run_cmd(func, cmd, verbose)


def dist_upgrade(assume_yes=True, use_sudo=True, verbose=True):
    """
    Same as `upgrade`, but Zypper will attempt to intelligently handle changing
    dependencies, installing new dependencies as needed.

    Args:
      assume_yes (bool): If `True`, Zypper will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    if assume_yes:
        yes = '-y'
    else:
        yes = ''

    func = use_sudo and sudo or run
    cmd = 'zypper dist-upgrade {0}'.format(yes)

    return _run_cmd(func, cmd, verbose)


def remove(packages, assume_yes=True, use_sudo=True,
           verbose=True):
    """
    Remove a package or list of packages from the remote host.

    Args:
      packages (list or str): The packages to install.
      purge (bool): If `True` any configuration files are deleted too.
        (Default: `False`)
      assume_yes (bool): If `True`, Zypper will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo (bool): If `True`, will use `sudo` instead of `run`.
        (Default: `True`)
      verbose (bool): If `False`, hide all output. (Default: `True`)
    """
    if not isinstance(packages, str):
        packages = ' '.join(packages)

    if assume_yes:
        yes = '-y'
    else:
        yes = ''

    func = use_sudo and sudo or run
    cmd = 'zypper remove {0} {1} {2}'.format(yes, purge, packages)

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
    cmd = 'zypper clean'

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
    cmd = 'apt-get autoclean'

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
    cmd = "rpm -q {0}".format(package)
    with settings(warn_only=True):
        installed = _run_cmd(func, cmd, verbose=False)
    if installed.find("install ok installed") > -1:
        return True
    return False
