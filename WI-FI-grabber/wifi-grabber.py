#   2021-January-20
#   by E.G

from platform import system
from os import listdir
from re import findall
from subprocess import run
from argparse import ArgumentParser, FileType


def main():
    parser = ArgumentParser(description='Grab saved WI-FI passwords')
    parser.add_argument('-o', '--outfile', type=FileType('w'),
                        help='Output results to file')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Supress console output')
    parser.add_argument('-n', '--noexit', action='store_true',
                        help='Do not close after finishing')
    args = parser.parse_args()

    os = system()
    if os.lower() == 'windows':
        result = grabWindows()
    elif os.lower() == 'linux':
        result = grabLinux()

    if args.outfile:
        args.outfile.write(result[1])

    if not args.quiet and result[0]:
        print(result[0])
    
    if args.noexit:
        input('Program finished. press return to exit.')


def grabWindows():
    try:
        capture = []
        raw = ''
        out = run('netsh wlan show profiles',
                  capture_output=True).stdout.decode()
        profiles = findall('    All User Profile     : (.*)\r', out)
        for profile in profiles:
            out = run('netsh wlan show profile "'+profile +
                      '" key=clear', capture_output=True).stdout.decode()
            passwords = findall('    Key Content            : (.*)\r', out)
            for password in passwords:
                capture.append([profile, password])
                raw = raw+profile+':'+password+'\n'
        return makeTable(capture), raw
    except:
        print('Failed to find any WI-FI passwords on Windows')


def grabLinux():
    try:
        profiles_dir = '/etc/NetworkManager/system-connections/'
        capture = []
        raw = ''
        connections = [f for f in listdir(
            profiles_dir) if f.endswith('.nmconnection')]
        for connection in connections:
            file = open(profiles_dir+connection, 'r').read()
            profile = findall('ssid=(.*)', file)
            password = findall('psk=(.*)', file)
            capture.append([profile[0], password[0]])
            raw = raw+profile[0]+':'+password[0]+'\n'
        return makeTable(capture), raw
    except:
        print('Failed to find any WI-FI passwords on Linux')


def makeTable(capture):
    try:
        longest = max(len(x) for sublist in capture for x in sublist)
        output = ''
        output = output+'='*(longest*2+17)+'\n'
        output = output+'| Name'+' ' * \
            (longest-2)+'| Password'+' '*(longest+2)+'|'+'\n'
        output = output+'+'+'-'*(longest*2+15)+'+'+'\n'
        for profile in capture:
            nl = len(profile[0])
            pl = len(profile[1])

            output = output+'| ' + \
                profile[0]+' '*((longest+2)-nl)+'| '+profile[1] + \
                ' '*((longest+10)-pl)+'|'+'\n'
            output = output+'-'*(longest*2+17)+'\n'
        return output
    except:
        print('No passwords found')


if __name__ == "__main__":
    main()
