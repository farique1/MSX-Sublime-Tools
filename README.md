# MSX Sublime Tools  
For Sublime Text 3  
  
**MSX Sublime Tools** was created to improve the experience of the **MSX Basic Dignified** project but also helps the creation of regular **MSX Basic** programs.  
  
>[**MSX Basic Dignified**](https://github.com/farique1/msx-basic-dignified) allows you to code MSX Basic programs using modern coding standards on your preferred editor, convert them to the old MSX Basic structure and load it into an MSX (emulated or not.)  
  
There tools are composed of:  
- A Syntax Highlight for the Dignified and one for the Classic version of MSX Basic.  
- Ocean and Monokai based Themes with special scopes for the project.  
- A Build System to convert and run the Dignified version and run the Classic one.  
- A Comment Preference for the Dignified version.  
  
To install, just clone this repo and copy all root files into an `MSX` folder inside the Sublime `Packages` folder (`~/Library/Application Support/Sublime Text 3/Packages/` on a Mac).  
  
## Syntax Highlight  
  
Two pretty decent syntax highlights, one for the Dignified version and one for the Classic version of MSX Basic.  
- The Dignified characteristics:  
  
`MSX Basic Dignified.sublime-syntax`  
```  
name: MSX Basic Dignified  
file_extensions: bad  
scope: source.msxbasicdignified  
```  
- The Classic characteristics:  
  
`MSX Basic.sublime-syntax`  
```  
name: MSX Basic  
file_extensions: bas  
scope: source.msxbasic  
```  
One of the biggest differences is the Dignified version expects the instructions and variables to be separated by spaces and the Classic accepts them typed together (as per MSX Basic standards).  
The Classic version also has all the Dignified specifics removed for simplicity but maintains useful ones like the labels highlight on its `REM` lines.  
  
Here is a preview of them side by side:  
![# Versions](https://github.com/farique1/MSX-Sublime-Tools/blob/master/Images/Versions.png)  
  
And here some specifics for the Dignified version:  
![# Highlights](https://github.com/farique1/MSX-Sublime-Tools/blob/master/Images/Highlights.png)  
  
  
1. `REM` scope extends as long as there are line breaks (these lines will be joined together into a single line after the conversion).  
2. The same goes for the `DATA` information; in this case a `_` line break is needed as a `:` denote the end of the instruction.  
3. Quotes explicitly expects a `_` to continue on the next line. MSX Basic support open quotes so a line feed will just end the quote.  
  
MSX Basic Dignified still has issues on some fringe cases so the syntax highlight will try to point some of these potential issues as well as some irregularities that are taken care by the conversion.  
  
4. Leading line numbers are issued automatically so they should not be on the Dignified code; they will be removed automatically with a warning. However numbers beginning a broken `REM` line after a `:` are improperly removed. Both cases are highlighted with a warning.  
5. `ENDIF`s alone on a line are automatically removed on the conversion. However `ENDIF` commands not alone are not removed (will generate a warning) and `ENDIF`s that are part of another command but are alone due to an line break (`_`) are improperly removed. Both cases are highlighted with a warning.  
6. Errors that stop the execution of the conversion are highlighted as errors.  
  
  
## Themes  
  
`MSX Monokai.tmTheme`  
A theme based on Monokai.  
  
`MSX Boxy Ocean.tmTheme`  
And a theme based on Boxy Ocean.  
  
They improve the MSX syntax highlight (Classic and Dignified) with scopes specific for the Dignified code: `define`, `declare`, labels, errors and warnings.  
  
## Build System  
  
The Dignified code can be converted and run straight from Sublime using **openMSX**.  
The Classic code can also run from Sublime, no need for a conversion here.  
  
>The build system only works on a Mac for now, mostly due to path differences.  
  
The builds will be available from the `Tools > Build System` menu and are called:  
  
*MSX Badig*  
*MSX Basic Run*  
  
When using the syntax scopes and extensions, Sublime will choose and use the correct one automatically.  
  
The build system is composed of the following files:  
```  
MSX Badig.sublime-build  
MSX Basic Run.sublime-build  
MSX Badig Build.ini  
MSX Badig Build.py  
MSX Badig Build.sublime-syntax  
```  
  
Before it can be used, however, some requirements  must be met:  
- An installed copy of **openMSX**.  
- An **openMSX** `savestate` file with the MSX booted up and disk drive capability must be made. This is necessary to speed things a little since Sublime will open a new instance of openMSX for each build.  
- If coding in the Dignified version, a copy of **MSX Basic Dignified** must also be present.  
- `MSX Badig Build.ini` must be set up with the path to **openMSX**, the `savestate` file and `msxbadig.py`.  
  
`MSX Badig Build.ini`  
```ini  
[DEFAULT]  
openmsx_filepath = /<path_to>/openmsx.app  
savestate_filepath = /<path_to>/savestate.oms  
msxbadig_filepath = /<path_to>/msxbadig.py  
```  
To run the build just press CTRL-B on Sublime.  
*Convert and Run* an *Convert Only* can be toggled by pressing CTRL-SHIFT-B on a Dignified code. There is no need for a conversion on the Classic code so it will always just *Run*.  
  
The build will convert the Dignified code using the default settings of **MSX Basic Dignified**, these can be configured in its own `.ini` file.  
By default the converted Classic code will be saved on the same path as the Dignified code with its name truncated to the first 8 characters and a `.bas` extension added.  
**openMSX** will then be opened with *throttle on*, load the `savestate`, mount the converted file folder as a disk and a `RUN "<converted_file>"+RETURN` command will be sent.  
Every build command will open a new instance of **openMSX**.  
  
Some of those options can be configured with *REM tags* on the Dignified code itself, just add the needed lines anywhere.  
>They can be toggled off just by adding another `#` at the start of each line.  
```ini  
##BB:export_path=/<path_where_to_save_the_converted_file>/  
##BB:export_file=<the_converted_file>  
##BB:convert_only=<True/False>  
##BB:throttle=<True/False>  
##BB:arguments=<msx_basic_dignified_command_line_arguments>  
```  
`##BB:export_path=`  
: The path where the converted code should be saved. This path will be mounted as a drive on **openMSX**  
  
`##BB:export_file=`  
: The name of the converted file. Better with an 8 character name and a `.bas` extension.  
  
`##BB:convert_only=`  
: `True` or `False`. If true will only convert the code, otherwise will convert and run. Overrides the Sublime build settings.  
  
`##BB:throttle=`  
: `True` or `False`. Force **openMSX** to open with or without *throttle on*.  
  
`##BB:arguments=`  
: Pass conversion arguments overriding the defaults and the `.ini` file on **MSX Basic Dignified**. The arguments are the same as the ones used on the command line and must be separated by commas.  
  
Sublime will display the build output on the console and highlight warnings and errors.  
  
## Comment Preference  
  
`MSX Comments.tmPreferences`  
  
Set `##` as the default hotkey comment.  
`##` is a Dignified comment that is not converted to the Classic code.  
There is no block comment but all lines selected will be commented.  
  
There is no Classic comment preference as I couldn't find a way to insert the `REM` or `'` after the line number.  
  
  
## Acknowledgements  
  
As always, all of this is offered as is, with no guaranties whatsoever. Use at your own discretion.  
Having said that, enjoy and send feedback.  
Thanks.  
