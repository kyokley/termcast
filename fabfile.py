from fabric import colors
from fabric import api as fab
from fabric import decorators
from fabric.contrib import files

from termcastTemplates import termcastTemplate, termcastPlayTemplate

import os, getpass

fab.env.colors = True

COMMANDS = ('sudo apt-get install ttyrec',
        )
SCRIPTS = ('termcast', 'termcast-play')

inetdConfTemplate = '''
telnet stream tcp4 nowait {user} /usr/sbin/tcpd /usr/bin/termcast-play
telnet stream tcp6 nowait {user} /usr/sbin/tcpd /usr/bin/termcast-play
'''


def write_file(filename, text, use_sudo=False):
    files.append(filename, text, use_sudo=use_sudo)

def write_sudo_file(filename, text):
    write_file(filename, text, use_sudo=True)

@fab.task
@decorators.hosts(['localhost'])
def install():
    user = getpass.getuser()
    installDir = os.getcwd()

    for command in COMMANDS:
        fab.local(command)

    casts = fab.prompt(colors.cyan('Specify directory where you want the '
                                      'casts to be stored'),
                           default=os.path.join(installDir, 'casts'))

    values = {'user': user,
              'installDir': installDir,
              'termcastPath': os.path.join(installDir, 'termcast'),
              'termcastPlayPath': os.path.join(installDir, 'termcast-play'),
              'casts': casts}

    try:
        fab.local('rm {}'.format(values['termcastPath']))
        fab.local('rm {}'.format(values['termcastPlayPath']))
    except:
        pass

    write_file(values['termcastPath'], termcastTemplate.format(**values))
    write_file(values['termcastPlayPath'], termcastPlayTemplate.format(**values))

    linkCommand = 'sudo ln -s {} /usr/bin'
    for script in SCRIPTS:
        try:
            fab.local(linkCommand.format(os.path.join(installDir, script)))
        except:
            pass

    inetdConfText = inetdConfTemplate.format(**values)

    write_sudo_file('/etc/inetd.conf', inetdConfText)
    fab.local('sudo /etc/init.d/openbsd-inetd restart')
    fab.local('chmod a+x {}'.format(values['termcastPath']))
    fab.local('chmod a+x {}'.format(values['termcastPlayPath']))
