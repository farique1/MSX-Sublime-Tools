"""

MSX Badig Build
v1.0
A build system to run MSX Basic Dignified source or tradicional
MSX Basic code on openMSX straight from Sublime Text 3.

Copyright (C) 2019 - Fred Rique (farique)
https://github.com/farique1/MSX-Sublime-Tools/
"""

import subprocess
import argparse
import ConfigParser
import os.path
import sys

openmsx_filepath = ''
savestate_filepath = ''
msxbadig_filepath = ''
throttle = True
arg = ['-fb'] * 24
arg_items = ''
output = ''

# Read command line arguments
parser = argparse.ArgumentParser(description='Convert MSX Basic Dignified source and run on openMSX')
parser.add_argument("file_path", help='The path to the oppened file to convert')
parser.add_argument("file_name", help='The oppened file to converted')
parser.add_argument("-classic", action='store_true', help='The file type: 0 Dignified(def), 1 Basic')
parser.add_argument("-convert", action='store_true', help='Do not run the code after conversion')
args = parser.parse_args()

export_path = args.file_path + '/'
export_file = os.path.splitext(args.file_name)[0][0:8] + '.bas'
classic_basic = args.classic
convert_only = args.convert


local_path = os.path.dirname(__file__) + '/'
try:
    with open(local_path + '/MSX Badig Build.ini') as f:
        pass
except IOError:
    print '*** MSX Badig Build.py: (20): .ini_not_found'
    print '    Execution_stoped'
    raise SystemExit(0)

# Read ini file
config = ConfigParser.ConfigParser()
config.sections()
config.read(local_path + '/MSX Badig Build.ini')
openmsx_filepath = config.get('DEFAULT', 'openmsx_filepath')
savestate_filepath = config.get('DEFAULT', 'savestate_filepath')
msxbadig_filepath = config.get('DEFAULT', 'msxbadig_filepath')

with open(args.file_path + '/' + args.file_name) as f:
    for n, line in enumerate(f):
        if line.startswith('##BB:export_path='):
            export_path = line.replace('##BB:export_path=', '').strip()
            if export_path[-1:] != '/':
                export_path += '/'
        if line.startswith('##BB:export_file='):
            export_file = line.replace('##BB:export_file=', '').strip()
        if line.startswith('##BB:throttle='):
            throttle = True if line.replace('##BB:throttle=', '').lower().strip() == 'true' else False
        if line.startswith('##BB:convert_only='):
            convert_only = True if line.replace('##BB:convert_only=', '').lower().strip() == 'true' else False
        if line.startswith('##BB:arguments='):
            arguments_line = n + 1
            arguments = line.replace('##BB:arguments=', '').strip()
            arguments = arguments.split(',')
            for num, item in enumerate(arguments):
                if num > 23:
                    break
                item2 = item
                item2 = item2.strip()
                item2 = item2.replace(' ', '=')
                item2 = '-fb' if item2 == "" else item2
                arg[num] = item2
                arg_items += ' ' + item2

if not classic_basic:
    print 'MSX Basic Dignified'
    print 'Converting ' + args.file_path + '/' + args.file_name
    print 'To ' + export_path + export_file
    print 'With ' + ('args' + arg_items if arg_items != '' else 'no args')
    # This... thing... down here? I know, I know Leave me alone!
    try:
        chama = ['python', msxbadig_filepath, args.file_path + '/' + args.file_name, export_path + export_file, '-fb', arg[0], arg[1], arg[2], arg[3], arg[4], arg[5],
                 arg[6], arg[7], arg[8], arg[9], arg[10], arg[11], arg[12], arg[13], arg[14], arg[15], arg[16], arg[17], arg[18], arg[19], arg[20], arg[21], arg[22], arg[23]]
        output = subprocess.check_output(chama).rstrip()
        print output
    except:
        print '*** ' + args.file_name + ': (' + str(arguments_line) + '): argument_error'
        print '    Execution_stoped'
        raise SystemExit(0)

else:
    export_path = args.file_path
    export_file = args.file_name

if 'Execution_stoped' in output or convert_only:
    print
    raise SystemExit(0)

print
print 'openMSX'
print 'Opeening ' + export_path + '/' + export_file
print
print "--- With throttle" if throttle else "--- Without throttle"

# openMSX <command>s like their spaces escaped
export_path = export_path.replace(' ', r'\ ')
export_file = export_file.replace(' ', r'\ ')

cmd = (openmsx_filepath + '/contents/macos/openmsx -control stdio -savestate ' + savestate_filepath)

proc = subprocess.Popen([cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

proc.stdin.write('<command>set renderer SDL</command>')
proc.stdin.flush()
print "---", proc.stdout.readline().rstrip()

proc.stdin.write('<command>diska eject</command>')
proc.stdin.flush()
print "---", proc.stdout.readline().rstrip()

proc.stdin.write('<command>diska insert ' + export_path + '</command>')
proc.stdin.flush()
print "---", proc.stdout.readline().rstrip()

if throttle:
    proc.stdin.write('<command>set throttle off</command>')
    proc.stdin.flush()
    print "---", proc.stdout.readline().rstrip()

proc.stdin.write('<command>type_via_keybuf run"' + export_file + '\\r</command>')
proc.stdin.flush()
print "---", proc.stdout.readline().rstrip()

print
