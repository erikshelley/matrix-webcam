# Upgrading an Older WSL Distribution

Ubuntu 20.04 and other older WSL distributions do not provide a supported Python version by default. To keep one Ubuntu distribution, upgrade the existing installation in place from 20.04 to 22.04, then from 22.04 to 24.04.

Before upgrading, back up the distribution from Windows PowerShell. Replace `<DistroName>` with the name from `wsl --list --verbose` (often `Ubuntu`):

    $ wsl --list --verbose
    $ wsl --shutdown
    $ wsl --export <DistroName> ubuntu-20.04-backup.tar

From Windows PowerShell, open the distribution:

    $ wsl -d <DistroName>

Inside the Ubuntu shell, check available disk space, held packages, and the current release before upgrading:

    $ df -h
    $ lsb_release -a
    $ apt-mark showhold

Do not upgrade if the root filesystem is near full (above about 80-90% used or with only a few GB free), if the release is not Ubuntu 20.04, or if `apt-mark showhold` lists packages. Free disk space first, investigate held packages before unholding them with `sudo apt-mark unhold <package-name>`, and do not skip releases. The first upgrade must start on 20.04; the second must start on 22.04. An empty `apt-mark showhold` result is expected.

Perform the first upgrade:

    $ sudo apt update
    $ sudo apt full-upgrade
    $ sudo dpkg --configure -a
    $ sudo apt -f install
    $ sudo apt autoremove
    $ sudo apt install update-manager-core
    $ sudo do-release-upgrade

After the first upgrade, exit the Ubuntu shell. From Windows PowerShell, restart WSL and reopen the distribution:

    $ wsl --shutdown
    $ wsl -d <DistroName>

Inside Ubuntu, verify the release and package state:

    $ lsb_release -a
    $ python3 --version
    $ sudo apt update
    $ sudo apt full-upgrade

Confirm that `lsb_release -a` reports Ubuntu 22.04 before repeating the upgrade steps to reach Ubuntu 24.04. Repeat the restart and verification steps after the final upgrade, then confirm that it reports Ubuntu 24.04. Test important tools, repositories, and files before deleting the export backup. The upgrade can require significant disk space and may disable third-party repositories. Ubuntu 20.04 is end-of-life, so its package sources may require adjustment before the first upgrade.

To roll back if the upgrade has problems, return to Windows PowerShell, unregister the upgraded distribution, and restore the export. `wsl --unregister` permanently deletes the current distribution, so only use it after confirming the backup archive exists:

    $ wsl --shutdown
    $ wsl --unregister <DistroName>
    $ wsl --import <DistroName> C:\WSL\<DistroName> ubuntu-20.04-backup.tar --version 2

From Windows PowerShell, open the restored distribution as its original Linux user:

    $ wsl -d <DistroName> -u <LinuxUser>

Use an empty directory for `C:\WSL\<DistroName>`. The restored distribution contains its original users and files; specify the original Linux username with `-u` on the first launch.