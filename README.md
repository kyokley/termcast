# termcast
Record and play back terminal sessions

## Installation
The install script can be run by calling:

```
bash install.sh
```

The script assumes openbsd-inetd is installed. If you are using a different inetd that still gets its configuration information from /etc/inetd.conf, then simply restarting the appropriate service should be good enough.

However, if you are using something like xinetd that uses a different inetd.conf, a new entry will need to be added to the conf file. The new lines that the install script adds to /etc/inetd.conf are provided here for reference.

```
telnet stream tcp4 nowait {user} /usr/sbin/tcpd /usr/bin/termcast-play
telnet stream tcp6 nowait {user} /usr/sbin/tcpd /usr/bin/termcast-play
```

## Usage
### Recording
```
termcast [file]
```
Recording a new termcast can be achieved by simply executing termcast on the command line. This will create a screen session that is being recorded. By default, the termcast is stored in the casts folder and named with the date and time the file was recorded. If the optional file argument is provided, this will be the name of the recorded file.

### Playback
```
termcast-play [file]
```
Playing a termcast can be achieved by running termcast-play. By default, this will play either a termcast that is currently being recorded or the most recently recorded termcast. If the optional file argument is given, that file will be played instead.

### Streaming
By default, termcast will stream the currently being recorded termcast or the most recently recorded termcast over port 23 on the recording machine. This can be done in many ways. A couple are given below:
```
nc 127.0.0.1 23
```
Or,
```
telnet 127.0.0.1 23
```

## Limitations
The script will play back in a screen with the same dimensions of the original terminal. This means that if the viewer is attempting to view a termcast in a terminal smaller than what it was recorded in, there may be issues in the formatting of the output.

## Issues
I've noticed that when streaming a previously recorded termcast using telnet, playback seems to start in the middle of the recording.
