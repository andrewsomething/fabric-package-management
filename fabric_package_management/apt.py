from fabric.api import hide, run, settings, sudo
from fabric.context_managers import shell_env
from fabric.contrib.files import exists


def _run_cmd(func, cmd, verbose):
    """
    Utility function to run commands respecting `use_sudo` and `verbose`.
    """
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        if verbose:
            return func(cmd)
        with settings(hide('everything')):
            return func(cmd)

def install(packages, assume_yes=True, no_install_recommends=False,
            install_suggests=False, use_sudo=True, verbose=True):
    """
    Install packages on the remote host via Apt.

    Args:
      packages (list or str): The packages to install.
      no_install_recommends (bool):
      install_suggests (bool):
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
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

    func = use_sudo and sudo or run
    cmd = 'apt-get install {0} {1} {2} {3}'.format(yes,
                                                   recommends,
                                                   suggests,
                                                   packages)

    return _run_cmd(func, cmd, verbose)


def update(use_sudo=True, verbose=True):
    """
    Update Apt's package index files on the remote host.

    Args:
    Args:
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
    """
    func = use_sudo and sudo or run
    cmd = 'apt-get update'

    return _run_cmd(func, cmd, verbose)


def upgrade(assume_yes=True, use_sudo=True, verbose=True):
    """
    Install the newest versions of all packages on the remote host.

    Args:
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
    """
    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    func = use_sudo and sudo or run
    cmd = 'apt-get upgrade {0}'.format(yes)

    return _run_cmd(func, cmd, verbose)

def dist_upgrade(assume_yes=True, use_sudo=True, verbose=True):
    """
    Same as `upgrade`, but Apt will attempt to intelligently handle changing
    dependencies, installing new dependencies as needed.

    Args:
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
    """
    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    func = use_sudo and sudo or run
    cmd = 'apt-get dist-upgrade {0}'.format(yes)

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
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
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

    func = use_sudo and sudo or run
    cmd = 'apt-get remove {0} {1} {2}'.format(yes, purge, packages)

    return _run_cmd(func, cmd, verbose)


def clean(use_sudo=True, verbose=True):
    """
    Clears out retrieved package files.

    Args:
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
    """
    func = use_sudo and sudo or run
    cmd = 'apt-get clean'

    return _run_cmd(func, cmd, verbose)


def autoclean(use_sudo=True, verbose=True):
    """
    Like `clean`, but only removes package files that can no longer
    be downloaded.

    Args:
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
    """
    func = use_sudo and sudo or run
    cmd = 'apt-get autoclean'

    return _run_cmd(func, cmd, verbose)


def autoremove(assume_yes=True, use_sudo=True, verbose=True):
    """

    Args:
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
    """

    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    func = use_sudo and sudo or run
    cmd = 'apt-get autoremove {0}'.format(yes)

    return _run_cmd(func, cmd, verbose)

def source(package, download_only=False, use_sudo=False, verbose=True):
    """
    Download a given source package.

    Args:
      package (str): The source package to download.
      download_only (bool): If `True`, the source package will not be
        unpacked. (Default: `False`)
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `False`)
      verbose: If `True`, hide all output. (Default: `True`)
    """

    if download_only:
        download = '--download-only'
    else:
        download = ''

    func = use_sudo and sudo or run
    cmd = 'apt-get source {0} {1}'.format(download, package)

    return _run_cmd(func, cmd, verbose)


def build_dep(package, assume_yes=True, use_sudo=True, verbose=True):
    """
    Install the build dependencies for a given source package.

    Args:
      assume_yes (bool): If `True`, Apt will assume "yes" as answer to all
        prompts and run non-interactively. (Default: `True`)
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `True`)
      verbose: If `True`, hide all output. (Default: `True`)
    """

    if assume_yes:
        yes = '--yes'
    else:
        yes = ''

    func = use_sudo and sudo or run
    cmd = 'apt-get build-dep {0} {1}'.format(yes, package)

    return _run_cmd(func, cmd, verbose)


def reboot_required(use_sudo=False, verbose=False):
    """
    Check if a reboot is required after intalling updates.

    Returns:
      bool: `True` if a reboot is required, `False` if not.
      use_sudo: If `True`, will use `sudo` instead of `run`. (Default: `False`)
      verbose: If `True`, hide all output. (Default: `False`)
    """
    return exists('/var/run/reboot-required', use_sudo=use_sudo,
                                              verbose=verbose)
