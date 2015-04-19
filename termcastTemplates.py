termcastTemplate = '''#!/bin/bash
CASTS={casts}
CURRENT="$CASTS/current"

mkdir -p $CASTS

touch $CURRENT
ttyrec -a "$CURRENT" -e "/usr/bin/screen -c {installDir}/screenrc"
killall telnet

if [ $# -eq 1 ]
then
    ARCHIVE="$CASTS/$1"
else
    ARCHIVE="$CASTS/$(date +%F-%T).ttyrec"
fi

mv $CURRENT $ARCHIVE
echo "Saved termcast (to $ARCHIVE)."
'''

termcastPlayTemplate = '''#!/bin/bash
CASTS={casts}
CURRENT="$CASTS/current"

clear
if [ $# -eq 1 ]
then
    FILENAME="$CASTS/$1"
    ttyplay "$FILENAME"
else
    if [ ! -e $CURRENT ]; then
        FILENAME=$CASTS/`ls "$CASTS" -1t | head -n 1`
        if [ ! -f $FILENAME ]; then
            echo "No termcasts"
            exit
        fi
        CURRENT=$FILENAME
        echo $CURRENT
        ttyplay "$CURRENT"
    else
        ttyplay -p "$CURRENT"
    fi
fi

echo "Termcast done"
'''
