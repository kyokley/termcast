from fabric import colors
from fabric import api as fab
from fabric import decorators
from fabric.contrib import files

import os, getpass

fab.env.colors = True

COMMANDS = ('sudo apt-get install ttyrec',
        )
SCRIPTS = ('termcast', 'termcast-play')

inetdConfTemplate = '''
telnet stream tcp4 nowait {user} /usr/sbin/tcpd /usr/bin/termcast-play
telnet stream tcp6 nowait {user} /usr/sbin/tcpd /usr/bin/termcast-play
'''

def write_sudo_file(filename, text):
    files.append(filename, text, use_sudo=True)

@fab.task
@decorators.hosts(['localhost'])
def install():
    user = getpass.getuser()
    installDir = os.getcwd()

    for command in COMMANDS:
        fab.local(command)

    values = {'user': user}

    linkCommand = 'sudo ln -s {src} /usr/bin'
    for script in SCRIPTS:
        fab.local(linkCommand.format(os.path.join(installDir, script)))

    inetdConfText = inetdConfTemplate.format(**values)

    write_sudo_file('/etc/inetd.conf', inetdConfText)
    fab.local('sudo /etc/init.d/openbsd-inetd')
