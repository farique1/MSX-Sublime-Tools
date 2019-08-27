"""
MSX Badig Build
v1.2
A build system to run MSX Basic Dignified source or tradicional
MSX Basic code on openMSX straight from Sublime Text 3.

Copyright (C) 2019 - Fred Rique (farique)
https://github.com/farique1/MSX-Sublime-Tools/

9-8-2019
No more savestates, emulator boots and with chosen (or default) machine and load disk extension if necesssary
Extension can be at slot A or B. Default A, add :SlotB after the name for slot B
Log output moved to function with more info
Settings on Dignified code ## to override machine and extension
Converted file now with .asc extension
Better error handling
"""

import subprocess
import argparse
import ConfigParser
import os.path

openmsx_filepath = ''
machine_name = ''  # 'Sharp_HB-8000_1.2' 'Sharp_HB-8000_1.2_Disk' 'Philips_NMS_8250'
disk_ext_name = ''  # 'Microsol_Disk'
disk_ext_slot = 'ext'
msxbadig_filepath = ''
using_machine = 'default machine'
throttle = True
show_output = True
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
export_file = os.path.splitext(args.file_name)[0][0:8] + '.asc'
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
machine_name = config.get('DEFAULT', 'machine_name')
disk_ext_name = config.get('DEFAULT', 'disk_ext_name')
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
        if line.startswith('##BB:override_machine='):
            machine_name = line.replace('##BB:override_machine=', '').strip()
        if line.startswith('##BB:override_extension='):
            disk_ext_name = line.replace('##BB:override_extension=', '').strip()
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

if machine_name != '':
    using_machine = machine_name
    machine_name = '-machine ' + machine_name

disk_ext = disk_ext_name.split(':')
disk_ext_name = disk_ext[0].strip()
if len(disk_ext) > 1:
    disk_ext_slot = 'extb' if disk_ext[1].lower().strip() == 'slotb' else disk_ext_slot

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
    raise SystemExit(0)


def output(show_output, step):
    if show_output:
        # proc.stdin.flush()
        log_out = proc.stdout.readline().rstrip()
        if '"nok"' in log_out or ' error: ' in log_out:
            proc.stdin.write('<command>quit</command>')
            print '***', log_out + ': ' + step
            print '    Execution_stopped'
            raise SystemExit(0)
        else:
            print '---', log_out + ': ' + step


print
print 'openMSX'
print 'Opeening ' + export_path + export_file
print 'As a ' + using_machine
print 'With ' + (disk_ext_name + ' extension at ' + disk_ext_slot if disk_ext_name != '' else 'no extension')
print 'Throttle ' + ('enabled' if throttle else 'disabled')
print

# openMSX <command>s like their spaces escaped
export_path = export_path.replace(' ', r'\ ')
export_file = export_file.replace(' ', r'\ ')


cmd = (openmsx_filepath + '/contents/macos/openmsx ' + machine_name + ' -control stdio')
proc = subprocess.Popen([cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

output(show_output, 'Initialized as ' + using_machine)

# proc.stdin.write('<command>set renderer SDL</command>')
# output(show_output, 'Show screen')

proc.stdin.write('<command>set throttle off</command>')
output(show_output, 'Turn throttle on')

proc.stdin.write('<command>debug set_watchpoint write_mem 0xfffe {[debug read "memory" 0xfffe] == 0} {set renderer SDL}</command>')
output(show_output, 'Set render SDL watchpoint')

proc.stdin.write('<command>debug set_watchpoint write_mem 0xfffe {[debug read "memory" 0xfffe] == 1} {set throttle on}</command>')
output(show_output, 'Set throttle on watchpoint')

if disk_ext_name != '':
    proc.stdin.write('<command>' + disk_ext_slot + ' ' + disk_ext_name + '</command>')
    output(show_output, 'Insert disk drive extension: ' + disk_ext_name + ' at ' + disk_ext_slot)

proc.stdin.write('<command>diska insert ' + export_path + '</command>')
output(show_output, 'insert folder as disk: ' + export_path)

proc.stdin.write('<command>set power on</command>')
output(show_output, 'Power on')

proc.stdin.write('<command>type_via_keybuf \\r\\r</command>')  # Disk ROM ask for date
output(show_output, 'Press return twice')

proc.stdin.write('<command>type_via_keybuf load"' + export_file + '\\r</command>')
output(show_output, 'type load"' + export_file)

proc.stdin.write('<command>type_via_keybuf poke-2,0\\r</command>')
output(show_output, 'type poke to render SLD')

if not throttle:
    proc.stdin.write('<command>type_via_keybuf poke-2,1\\r</command>')
    output(show_output, 'type poke to turn throttle off')

proc.stdin.write('<command>type_via_keybuf cls:run\\r</command>')
output(show_output, 'type cls and run')

print
