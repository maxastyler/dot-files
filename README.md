# dot-files
A collection of my dot files with an installer.

##Requirements

Python3 for the installer. Dex for autostarting certain programs. Conky, py3status, clipit, nm-applet, volumeicon, dmenu, and a few other things.

## Installation

You can symlink the files manually with ln -s [file] [place to put file], or just use the setup.py script. 
If using python setup.py install, the script automatically backs up current configs to a folder ~/.mtyler_dotfiles_backup/
Using python setup.py uninstall will restore any files backed up to their original places, and delete any other files that were installed with this. It also deletes the .mtyler_dotfiles_backup folder.
