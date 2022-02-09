#!/usr/bin/env python3
"""
MSX Badig Build
v1.5
A Sublime Text 4 build system to convert MSX Basic Dignified to traditional MSX Basic and run on openMSX
or tokenize and run ASCII MSX Basic on openMSX.

Copyright (C) 2019-2022 - Fred Rique (farique)
https://github.com/farique1/MSX-Sublime-Tools

MSX Basic Dignified at
https://github.com/farique1/msx-basic-dignified

MSX Basic Tokenizer at
https://github.com/farique1/MSX-Basic-Tokenizer

Installation notes on the README.md

New: 1.5 03/12/2021
    WINDOWS COMPATIBILITY YEY!
        Individual Windows and Mac paths on the .INI file
        os.path() operations to improve compatibility across systems
    Changed .INI section names
"""

import os.path
import platform
import argparse
import subprocess
import configparser

msxbadig_filepath = ''      # Path to MSX Basic Dignified ('' = local path)
batoken_filepath = ''       # Path to MSX Basic Tokenizer ('' = local path)
openbatoken_filepath = ''   # Path to openMSX Basic Tokenizer ('' = local path)
openmsx_filepath = ''       # Path to openMSX ('' = local path)
machine_name = ''           # openMSX machine to open, eg: 'Sharp_HB-8000_1.2' 'Sharp_HB-8000_1.2_Disk' 'Philips_NMS_8250'
disk_ext_name = ''          # openMSX extension to open, eg: 'Microsol_Disk:SlotB'
throttle = False            # Run openMSX with throttle enabled
show_output = True          # Show the openMSX stderr output
monitor_exec = False        # Monitor the code execution on openMSX
tokenize = False            # Tokenize the ASCII code
tokenize_tool = 'b'         # Tool used to tokenize the ASCII code: b-MSX Basic Tokenizer(def) o-openMSX Basic Tokenizer
tokenize_stop = True        # Stop the execution on tokenize errors (keeps the ASCII version)
verbose_level = 3           # Show processing status: 0-silent 1-+erros 2-+warnings 3-+steps 4-+details

is_windows = platform.system() == "Windows"  # Get the operating system
python_app = 'python' if is_windows else 'python3'


def show_log(line, text, level, **kwargs):
    bullets = ['', '*** ', '  * ', '--- ', '  - ', '    ']

    if line != '':
        line_num, line_alt, line_file = line
    else:
        line_num, line_file = '', ''

    show_file = [True, False]

    try:
        bullet = kwargs['bullet']
    except KeyError:
        bullet = level

    try:
        show_file = kwargs['show_file']
    except KeyError:
        show_file = False

    display_file_name = ''
    if show_file and line_file != '':
        display_file_name = included_dict[line_file] + ': '

    line_num = '(' + str(line_num) + '): ' if line_num != '' else ''

    if verbose_level >= level:
        print(bullets[bullet] + display_file_name + line_num + text)

    if bullet == 1 and not show_file:
        print('    Execution_stoped')
        print()
        raise SystemExit(0)


show_log('', 'MSX Badig Build', 3, bullet=0)

parser = argparse.ArgumentParser(description='Convert MSX Basic Dignified source and run on openMSX')
parser.add_argument("file_path", help='The path to the opened file to convert')
parser.add_argument("file_name", help='The opened file to converted')
parser.add_argument("-classic", action='store_true', help='The flavor of Basic to process')
parser.add_argument("-convert", action='store_true', help='Do not run the code after conversion')
parser.add_argument("-monitor", default=monitor_exec, action='store_true', help='Monitor the execution on the emulator')
parser.add_argument("-tokenize", default=tokenize, action='store_true', help='Tokenize the ASCII code')
parser.add_argument("-list", action='store_true', help='Save a .mlt list file')
args = parser.parse_args()

export_path = args.file_path
export_file = os.path.splitext(args.file_name)[0] + '.asc'
classic_basic = args.classic
convert_only = args.convert
monitor_exec = args.monitor
tokenize = args.tokenize
save_list = args.list
file_load = args.file_name

local_path = os.path.split(os.path.abspath(__file__))[0]
ini_path = os.path.join(local_path, 'MSX Badig Build.ini')
if os.path.isfile(ini_path):
    ini_section = 'WINPATHS' if is_windows else 'MACPATHS'
    config = configparser.ConfigParser()
    config.sections()
    try:
        config.read(ini_path)
        msxbadig_filepath = config.get(ini_section, 'msxbadig_filepath') if config.get(ini_section, 'msxbadig_filepath') else msxbadig_filepath
        batoken_filepath = config.get(ini_section, 'batoken_filepath') if config.get(ini_section, 'batoken_filepath') else batoken_filepath
        openbatoken_filepath = config.get(ini_section, 'openbatoken_filepath') if config.get(ini_section, 'openbatoken_filepath') else openbatoken_filepath
        openmsx_filepath = config.get(ini_section, 'openmsx_filepath') if config.get(ini_section, 'openmsx_filepath') else openmsx_filepath
        machine_name = config.get('CONFIGS', 'machine_name') if config.get('CONFIGS', 'machine_name') else machine_name
        disk_ext_name = config.get('CONFIGS', 'disk_ext_name') if config.get('CONFIGS', 'disk_ext_name').strip() else disk_ext_name
        throttle = config.getboolean('CONFIGS', 'throttle') if config.get('CONFIGS', 'throttle') else throttle
        monitor_exec = config.getboolean('CONFIGS', 'monitor_exec') if config.get('CONFIGS', 'monitor_exec') else monitor_exec
        tokenize = config.getboolean('CONFIGS', 'tokenize') if config.get('CONFIGS', 'tokenize') else tokenize
        tokenize_tool = config.get('CONFIGS', 'tokenize_tool') if config.get('CONFIGS', 'tokenize_tool') else tokenize_tool
        tokenize_stop = config.getboolean('CONFIGS', 'tokenize_stop') if config.get('CONFIGS', 'tokenize_stop') else tokenize_stop
        verbose_level = config.getint('CONFIGS', 'verbose_level') if config.get('CONFIGS', 'verbose_level') else verbose_level
    except (ValueError, configparser.NoOptionError) as e:
        show_log('', '', 1, bullet=0)
        show_log('', 'MSX Badig Build.ini: ' + str(e), 1)

tokenize_tool = 'O' if tokenize_tool.upper() == 'O' else 'B'

call_monitor_tcl = ''
valid_args = ['-ls', '-lp', '-lz', '-rh', '-cs', '-gs', '-uo', '-bl', '-lg', '-sl', '-ll', '-nr', '-cr',
              '-ki', '-nc', '-cp', '-tg', '-tr', '-of', '-el', '-tt', '-vs', '-vb', '-exe', '-frb', '-ini']
arg_num = len(valid_args)
arg = ['-frb'] * arg_num
arg[arg_num - 2] = '-vb=' + str(verbose_level)
arg[arg_num - 3] = '-tt=' + tokenize_tool.upper()
disk_ext_slot = 'ext'
using_machine = 'default machine'
output = ''
btoutput = ''
arguments_line = ''
line_chama = ''
line_list = {}
included_dict = {}

if msxbadig_filepath == '':
    msxbadig_filepath = os.path.join(local_path, 'MSXBadig.py')
if batoken_filepath == '':
    batoken_filepath = os.path.join(local_path, 'MSXBatoken.py')
if openbatoken_filepath == '':
    openbatoken_filepath = os.path.join(local_path, 'openMSXBatoken.py')
if openmsx_filepath == '':
    openmsx_filepath = local_path
if tokenize_tool == 'O':
    batoken_filepath = openbatoken_filepath

show_log('', ''.join(['Building ', os.path.join(args.file_path, args.file_name)]), 3, bullet=0)
show_log('', '', 3, bullet=0)
show_log('', ''.join([('Classic Basic' if classic_basic else 'Basic Dignified')]), 3)
if classic_basic:
    label_log = 'Tokenize only' if tokenize and convert_only and not save_list else \
        'Tokenize and save list' if tokenize and convert_only and save_list else \
        'Tokenize and run' if tokenize and not convert_only and not save_list else 'Run'
if not classic_basic:
    label_log = 'Default' if monitor_exec and not convert_only else \
        'Convert only' if not monitor_exec and convert_only else "Don't monitor"
show_log('', label_log, 3, bullet=5)

if save_list and tokenize_tool == 'O':
    show_log('', 'openMSX Basic Tokenizer does not save lists', 2)

if not os.path.isfile(msxbadig_filepath) and not classic_basic:
    show_log('', ''.join(['MSX_Basic_Dignified.py_not_found: ', msxbadig_filepath]), 1)  # Exit

if not os.path.isfile(openbatoken_filepath) and (tokenize and tokenize_tool == 'O'):
    show_log('', ''.join(['openMSX_Basic_tokenizer.py_not_found: ', openbatoken_filepath]), 1)  # Exit

if not os.path.isfile(batoken_filepath) and (tokenize and tokenize_tool == 'B'):
    show_log('', ''.join(['MSX_Basic_tokenizer.py_not_found: ', batoken_filepath]), 1)  # Exit

if is_windows:
    if not os.path.isfile(openmsx_filepath) and (not convert_only or monitor_exec):
        show_log('', ''.join(['openMSX_not_found: ', openmsx_filepath]), 1)  # Exit
else:
    if not os.path.isdir(openmsx_filepath) and (not convert_only or monitor_exec):
        show_log('', ''.join(['openMSX_not_found: ', openmsx_filepath]), 1)  # Exit


show_log('', '', 3, bullet=5)

with open(os.path.join(args.file_path, args.file_name), encoding='latin1') as f:
    for n, line in enumerate(f):
        if line.startswith('##BB:export_path='):
            export_path = line.replace('##BB:export_path=', '').strip()
        if line.startswith('##BB:export_file='):
            export_file = line.replace('##BB:export_file=', '').strip()
        if line.startswith('##BB:throttle='):
            throttle = True if line.replace('##BB:throttle=', '').lower().strip() == 'true' else False
        if line.startswith('##BB:convert_only='):
            convert_only = True if line.replace('##BB:convert_only=', '').lower().strip() == 'true' else False
        if line.startswith('##BB:monitor_exec='):
            monitor_exec = True if line.replace('##BB:monitor_exec=', '').lower().strip() == 'true' and not convert_only else False
        if line.startswith('##BB:override_machine='):
            machine_name = line.replace('##BB:override_machine=', '').strip()
        if line.startswith('##BB:override_extension='):
            disk_ext_name = line.replace('##BB:override_extension=', '').strip()
        if line.startswith('##BB:arguments='):
            arguments_line = n + 1
            arguments = line.replace('##BB:arguments=', '').strip()
            arguments = arguments.split(',')
            for num, item in enumerate(arguments):
                if num > arg_num - 5:  # args [arg_num-4], [arg_num-3], [arg_num-2] and [arg_num-1] are reserved to -tt, -vb, -exe and -frb
                    break
                item2 = item
                item2 = item2.strip()
                item2 = item2.replace(' ', '=')
                if item2.split('=')[0] not in valid_args:
                    show_log('', ' '.join(['invalid_argument:', item2]), 1)
                if item2.split('=')[0] == '-vb':
                    try:
                        verbose_level = int(item2.split('=')[1])
                    except IndexError:
                        show_log('', ' '.join(['invalid_argument_value:', '-vb']), 1)
                    arg[arg_num - 2] = item2
                    item2 = '-frb'
                if item2.split('=')[0] == '-tt':
                    try:
                        tokenize_tool = item2.split('=')[1].upper()
                    except IndexError:
                        show_log('', ' '.join(['invalid_argument_value:', '-tt']), 1)
                    arg[arg_num - 3] = item2
                    item2 = '-frb'
                arg[num] = item2

if monitor_exec:
    if os.path.isfile(os.path.join(local_path, 'openMSXoutput.tcl')):
        call_monitor_tcl = ['-script', os.path.join(local_path, 'openMSXoutput.tcl')]
        arg[arg_num - 1] = '-exe'
    else:
        show_log('', ''.join(['openMSXoutput.tcl_script_not_found_(monitoring_disabled)']), 2)
        monitor_exec = False

if machine_name != '':
    using_machine = machine_name
    machine_name = ['-machine', machine_name]

disk_ext = disk_ext_name.split(':')
disk_ext_name = disk_ext[0].strip()
if len(disk_ext) > 1:
    disk_ext_slot = 'extb' if disk_ext[1].lower().strip() == 'slotb' else disk_ext_slot

if not classic_basic:
    args_token = list(set(arg))
    show_log('', 'MSX Basic Dignified', 3, bullet=0)
    show_log('', ''.join(['Converting ', os.path.join(args.file_path, args.file_name)]), 3, bullet=0)
    show_log('', ''.join(['To         ', os.path.join(export_path, export_file)]), 3, bullet=0)
    show_log('', ''.join(['With args ', ' '.join(args_token)]), 3, bullet=0)
    try:
        # This... thing... here? I know, I know Leave me alone!
        chama = [python_app, '-u', msxbadig_filepath, os.path.join(args.file_path, args.file_name), os.path.join(export_path, export_file)]
        chama.extend(arg)
        output = subprocess.check_output(chama, encoding='utf-8')
        for line in output:
            line_chama += line
            if line == '\n':
                if 'linelst-' in line_chama:
                    line_get = line_chama.replace('linelst-', '').split(',')
                    line_list[line_get[0]] = [line_get[1].rstrip(), line_get[2].rstrip()]
                elif 'export_file-' in line_chama:
                    export_file = line_chama.replace('export_file-', '').strip()
                elif 'includedict-' in line_chama:
                    included_get = line_chama.replace('includedict-', '').strip()
                    included_get = included_get.split(',')
                    included_dict[included_get[0]] = included_get[1]
                elif 'Tokenizing_aborted' in line_chama:
                    show_log('', line_chama.rstrip(), 1, bullet=0)
                    tokenize = False
                else:
                    show_log('', line_chama.rstrip(), verbose_level, bullet=0)
                line_chama = ''

    except subprocess.CalledProcessError:
        show_log('', ''.join([args.file_name, ': (', str(arguments_line), '): argument_error']), 1)  # Exit

else:
    export_path = args.file_path
    export_file = args.file_name
    if tokenize:
        list_arg = ['-frb'] * 3
        list_arg[2] = '-vb=' + str(verbose_level)
        if save_list and tokenize_tool == 'B':
            list_arg[1] = '-el'
        btline = ''
        args_token = list(set(list_arg))
        name_prefix = '' if tokenize_tool == 'B' else 'open'
        show_log('', name_prefix + 'MSX Basic Tokenizer', 3, bullet=0)
        show_log('', ''.join(['Converting ', os.path.join(export_path, export_file)]), 3, bullet=0)
        show_log('', ''.join(['To         ', os.path.join(export_path, os.path.splitext(export_file)[0]) + '.bas']), 3, bullet=0)
        show_log('', ''.join(['With ', 'args ', ' '.join(args_token)]), 3, bullet=0)
        if os.path.isfile(batoken_filepath):
            batoken = [python_app, '-u', batoken_filepath, os.path.join(export_path, export_file), list_arg[0], list_arg[1], list_arg[2]]
            btoutput = subprocess.check_output(batoken, encoding='utf-8')
            for line in btoutput:
                btline += line
                if line == '\n':
                    if 'Tokenizing_aborted' in btline:
                        show_log('', btline.rstrip(), 1, bullet=0)
                        tokenize = False
                    else:
                        show_log('', btline.rstrip(), verbose_level, bullet=0)
                        btline = ''
            if tokenize:
                export_file = os.path.splitext(export_file)[0] + '.bas'
        else:
            show_log('', ''.join(['MSX_Basic_Tokenizer_not_found: ', batoken_filepath]), 2)

if ('Tokenizing_aborted' in output or 'Tokenizing_aborted' in btoutput) and not tokenize:
    show_log('', 'Execution_stoped', 1, bullet=5)
    show_log('', '', 1, bullet=0)
    raise SystemExit(0)

if 'Execution_stoped' in output or 'Execution_stoped' in btoutput:
    show_log('', '', 1, bullet=0)
    raise SystemExit(0)

if convert_only:
    raise SystemExit(0)


def output(show_output, has_input, step):
    if show_output:
        log_out = proc.stdout.readline().rstrip() if has_input else ''
        log_out = log_out.replace('&quot;', '"')
        log_out = log_out.replace('&apos;', "'")
        if '"nok"' in log_out or ' error: ' in log_out:
            log_out = log_out.replace('<reply result="nok">', '')
            proc.stdin.write('<command>quit</command>')
            show_log('', ''.join([step]), 3)
            if 'invalid command name "ext' in log_out:
                show_log('', ''.join(['Machine probably missing a slot']), 2)
            show_log('', ''.join([log_out]), 1)  # Exit
        elif '<log level="warning">' in log_out:
            log_warning = log_out.replace('<log level="warning">', '')
            log_warning = log_warning.replace('</log>', '')
            log_out = log_out.split('<log')[0]
            log_comma = '' if log_out == '' else ': '
            if step + log_comma + log_out != '':
                show_log('', ''.join([step, log_comma, log_out]), 3)
            show_log('', ''.join([log_warning]), 2)
            output(show_output, True, '')
        else:
            log_out = log_out.replace('<openmsx-output>', '')
            log_out = log_out.replace('</openmsx-output>', '')
            log_out = log_out.replace('<reply result="ok">', '')
            log_out = log_out.replace('</reply>', '')
            log_comma = '' if log_out == '' else ': '
            if step + log_comma + log_out != '':
                show_log('', ''.join([step, log_comma, log_out]), 3)


show_log('', 'openMSX', 3, bullet=0)
show_log('', ''.join(['Opeening ', os.path.join(export_path, export_file)]), 3, bullet=0)
show_log('', ''.join(['As a ', using_machine]), 3, bullet=0)
show_log('', ''.join(['With ', disk_ext_name, (' extension at ' + disk_ext_slot if disk_ext_name != '' else 'no extension')]), 3, bullet=0)
show_log('', ''.join(['Throttle ', ('enabled' if throttle else 'disabled')]), 3, bullet=0)
show_log('', '', 3, bullet=0)

crop_export = os.path.splitext(export_file)[0][0:8] + os.path.splitext(export_file)[1]
crop_export = crop_export.replace(' ', '_')

if tokenize_tool == 'O':
    export_file = crop_export

list_dir = os.listdir(export_path)
list_export = [x for x in list_dir if
               x.lower() != export_file.lower()
               and os.path.splitext(x)[0][0:8].replace(' ', '_').lower()
               + os.path.splitext(x)[1].replace(' ', '_').lower()
               == crop_export.lower()]
if list_export:
    show_log('', ' '.join(['MSX_disk_name_format_conflict', ', '.join(list_export), '=', export_file, '(' + crop_export + ')']), 1)  # Exit

export_path = export_path.replace(' ', r'\ ')

if is_windows:
    export_path = export_path.replace('\\', '/')  # cmd apparently needs forward slashes even on Windows
    cmd = [openmsx_filepath, '-control', 'stdio']
else:
    cmd = [os.path.join(openmsx_filepath, 'contents', 'macos', 'openmsx'), '-control', 'stdio']

if machine_name != '':
    cmd.extend(machine_name)
if monitor_exec:
    cmd.extend(call_monitor_tcl)

proc = subprocess.Popen(cmd, bufsize=1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', close_fds=True)

endline = '\r\n'

output(show_output, True, 'openMSX initialized as ' + using_machine)

# proc.stdin.write('<command>set renderer SDL</command>' + endline)
# output(show_output, True, 'Show screen')

proc.stdin.write('<command>set throttle off</command>' + endline)
output(show_output, True, 'Turn throttle on')

proc.stdin.write('<command>debug set_watchpoint write_mem 0xfffe {[debug read "memory" 0xfffe] == 0} {set renderer SDL}</command>' + endline)
output(show_output, True, 'Set render SDL watchpoint')

proc.stdin.write('<command>debug set_watchpoint write_mem 0xfffe {[debug read "memory" 0xfffe] == 1} {set throttle on}</command>' + endline)
output(show_output, True, 'Set throttle on watchpoint')

if disk_ext_name != '':
    proc.stdin.write('<command>' + disk_ext_slot + ' ' + disk_ext_name + '</command>' + endline)
    output(show_output, True, 'Insert disk drive extension: ' + disk_ext_name + ' at ' + disk_ext_slot)

proc.stdin.write('<command>diska insert ' + export_path + '</command>' + endline)
output(show_output, True, 'Insert folder as disk: ' + export_path)

proc.stdin.write('<command>set power on</command>' + endline)
output(show_output, True, 'Power on')

proc.stdin.write('<command>type_via_keybuf \\r\\r</command>' + endline)  # Disk ROM ask for date, two enter to skip
output(show_output, True, 'Press return twice')

proc.stdin.write('<command>type_via_keybuf load"' + crop_export + '\\r</command>' + endline)
output(show_output, True, 'Type load"' + crop_export)

proc.stdin.write('<command>type_via_keybuf poke-2,0\\r</command>' + endline)
output(show_output, True, 'Type poke to render SLD')

if not throttle:
    proc.stdin.write('<command>type_via_keybuf poke-2,1\\r</command>' + endline)
    output(show_output, True, 'Type poke to turn throttle off')

proc.stdin.write('<command>type_via_keybuf cls:run\\r</command>' + endline)
output(show_output, True, 'Type cls and run')

show_log('', '', 3, bullet=0)

if monitor_exec and is_windows:
    show_log('', 'Execution monitoring not yet supported on Windows', 2)
    show_log('', '', 1, bullet=0)
elif monitor_exec:
    show_log('', 'Monitoring execution', 3, bullet=0)
    show_log('', '', 3, bullet=0)

    for line in iter(proc.stdout.readline, b''):
        poll = proc.poll()
        if poll is not None:
            print()
            raise SystemExit(0)
        if '\x07' in line and '\x0c' not in line:
            line_out = line.replace('\x0d', '').replace('\x07', '').rstrip()
            current_line_list = line_out.split(' ')[len(line_out.split(' ')) - 1].rstrip()
            if line_out[:5] == 'Parei' or line_out[:5] == 'Break':
                bullet = 3
            elif current_line_list in line_list:
                bullet = 1
            else:
                bullet = 2

            if current_line_list in line_list:
                line_exec = line_list[current_line_list][0], '', line_list[current_line_list][1]
                show_log(line_exec, ''.join([line_out]), 1, bullet=bullet, show_file=True)
            else:
                show_log('', ''.join([line_out]), 2, bullet=bullet, show_file=True)

    # proc.wait()
    show_log('', '', 1, bullet=0)
