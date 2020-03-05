  
<img src="https://github.com/farique1/MSX-Sublime-Tools/blob/master/Images/GitHub_SublimeTools_Logo-02.png" alt="MSX Sublime Tools" width="290" height="130">  
  
# MSX Sublime Tools  
**v1.5**  
For **Sublime Text 3**  
  
**MSX Sublime Tools** are a set of tools developed for Sublime Text 3 created to improve the experience of working with **MSX Basic Dignified** and regular **MSX Basic** programs.  
  
>[**MSX Basic Dignified**](https://github.com/farique1/msx-basic-dignified) is a 'dialect' of MSX Basic using modern coding style and standards that can be composed on any text editor and converted to the traditional MSX Basic to be executed.  
  
The tools are:  
- A **Build System** for the Dignified and traditional versions of MSX Basic with conversion, tokenization and execution monitoring capabilities.  
- **Syntax Highlight**s for the Dignified and traditional versions of MSX Basic.  
- **Theme**s based on Boxy Ocean and Monokai with special scopes for both Basic versions.  
- A **Theme** simulating the blue MSX 1 screen and accompanying **MSX Screen 0 font**.  
- **Snippets** for the Dignified version of MSX Basic.  
- A **Comment Preference** for the Dignified version.  
  
To install, just clone this repo and copy all root files into an `MSX` folder inside the Sublime `Packages` folder (`~/Library/Application Support/Sublime Text 3/Packages/` on a Mac).  
  
The Dignified Basic version uses a `.bad` extension and the traditional ASCII Basic an `.asc` one.  
  
## Build System  
  
The Dignified code can be converted, tokenized and run straight from Sublime using **MSX Basic Dignified**, **openMSX** and one of the **MSX Basic Toknizer**s. It can also have its execution monitored for Basic errors and have the offending Dignified lines tagged back on Sublime.  
Traditional MSX Basic can also be tokenized and run from Sublime, no monitoring here unfortunately.  
A list file similar to the ones exported by assemblers with the tokens alongside the ASCII code and some statistics can also be exported (see an eaxample at [**MSX Basic Tokenizer**](https://github.com/farique1/MSX-Basic-Tokenizer)).  
Sublime will display the build output on the console and highlight warnings and errors.  
  
>When using **openMSX** to execute or monitor the code be aware that the saving folder will be mounted on the MSX as a disk and all constrains of that filesystem apply including file size, name size, lack of spaces on the names, etc. (the build system will try to mitigate some of these but caution is the better approach.)  
  
>The build system only works on a Mac for now mostly due to path differences and the way **openMSX** is executed.  
  
>The Build System uses Python 3.8.  
  
  
The build system is composed of the following files:  
```  
MSX Badig Build.py  
MSX Badig Build.ini  
MSX Badig Build.sublime-syntax  
MSX Basic Dignified.sublime-build  
MSX Basic.sublime-build  
openMSXoutput.tcl  
```  
  
Depending on what functionality is required the aforementioned programs need to be installed:  
  
- If coding in the Dignified flavour, a copy of **MSX Basic Dignified** is needed.  
- **MSX Basic Tokenizer** or **openMSX Basic (de)Tokenizer** are needed for tokenized output and list export.  
- To run and monitor the program execution, an installed copy of **openMSX** with a machine supporting disk drive is needed.  
  
The path to these programs can be set up on the code itself or on `MSX Badig Build.ini`.  The deafault behaviour of the build system in addition to these can also be setup on ***REM tags*** on the Dignified code. Each setup method have a priority higher than the one before.  
  
### Seting up  
  
**`MSX Badig Build.ini`**  
  
The only configuration necessary on the `.ini` file are the paths to the support programs being used and any modification to the default behaviour of the build system. All other settings can be left blank.  
  
```ini  
[DEFAULT]  
msxbadig_filepath = [/path_to/msxbadig.py]  
batoken_filepath = [/path_to/msxbatoken.py]  
openbatoken_filepath = [/path_to/openmsxbatoken.py]  
openmsx_filepath = [/path_to/openmsx.app]  
machine_name = [optional alternative machine name]  
disk_ext_name = [optional disk extension]  
monitor_exec = [true,false]  
throttle = [true,false]  
tokenize = [true,false]  
tokenize_tool = [b,o]  
tokenize_stop = [true,false]  
verbose_level = [#]  
```  
  
`msxbadig_filepath = `  
The path to **MSX Basic Dignified**  
  
`batoken_filepath = `  
The path to **MSX Basic Tokenizer**  
  
`openbatoken_filepath = `  
The path to **openMSX Basic (de)Tokenizer**  
  
`openmsx_filepath = `  
The path to **openMSX**  
  
`machine_name =` Default: none (run **openMSX** with the default machine)  
The name of a machine that will be used instead of the default one on **openMSX**.  
  
`disk_ext_name =` Default: none (no disk extension are loaded)  
The name of a disk drive extension in case the selected machine does have a disk drive. Will be inserted on the *Slot A* by default, can be inserted in *Slot B* by using `:SlotB` at the end.  
  
`monitor_exec =` `true` or `false` Default: `true`  
Enable or disable the execution monitoring of the code on **openMSX** after conversion. The monitoring catch errors in Basic and tag the offending Dignified line on Sublime.  
  
`throttle =` `true` or `false` Default: `false`  
Force **openMSX** to open with or without *throttle* activated.  
  
`tokenize =` `true` or `false` Default: `true`  
Enable or disable saving a tokenized version of the code.  
  
`tokenize_tool =` `b` or `o` Default: `b`  
The program used to tokenize the code.  
`b` = **MSX Basic Tokenizer**  
`o` = **openMSX Basic (de)Tokenizer**  
  
`tokenize_stop =` `true` or `false` Default: `true`  
If `true` will stop the build on tokenization errors. If `false` will try to continue the build process with the ASCII version of the code (the ASCII version is always saved before tokenization).  
  
`verbose_level =` `#` Default: `3`  
Set the level of feedback given. Will cascade down to the support programs.  
`0` show nothing, `1` errors, `2` errors and warnings, `3` errors, warnings and steps and `4` errors, warnings, steps and details.  
  
***REM tags***  
  
Each support program have its own configurations that can be changed on their installation and `.ini` files. Some of these, however, can be forced using *REM tags* on the Dignified code itself, just add the needed lines anywhere. The *REM tags* will override all other settings including the build variant ones.  
  
```ini  
##BB:export_file=<the_converted_file>  
##BB:export_path=<path_where_to_save_the_converted_file>  
##BB:override_machine=<optional alternate machine name>  
##BB:override_extension=<optional disk extension[:SlotB]>  
##BB:monitor_exec=<true,false>  
##BB:throttle=<true,false>  
##BB:convert_only=<true,false>  
##BB:arguments=<msx_basic_dignified_command_line_arguments>  
```  
  
>There is no need to delete a line of REM tag when not using it. They can be toggled off just by changing the `##BB:` prefix (to `## BB:` for instance.)  
  
`##BB:export_file=`  
The name of the converted ASCII file, better with an 8 character name and a `.asc` extension to conform with the standards. The tokenized version will have a `.bas` extension.  
  
`##BB:export_path=`  
The path where the converted code should be saved. This path will be mounted as a drive on **openMSX** so be careful.  
  
`##BB:override_machine=`  
`##BB:override_extension=`  
`##BB:monitor_exec=`  
`##BB:throttle=`  
The same as on the `MSX Badig Build.ini`.  
  
`##BB:convert_only=`  
`true` or `false`. If true will only convert the code otherwise will convert and run.  
  
`##BB:arguments=`  
Pass arguments to **MSX Basic Dignified**, they are the same as the ones used on the command line and must be separated by commas.  
Arguments can be used here to complement the *REM tags*.  
- They can force the use of one or the other tokenization program: `-tt <b,o>` works the same way as on the `.ini`'s `tokenize_tool`.  
- Dictate if a tokenized, ASCII or both versions should be saved: `-of <t,a,b>` tells the build system to export a tokenized, an ASCII or both versions respectively.  
 - Or if a `.mlt` list file should be exported: `-el [#]` export a list file (for more information see **MSX Basic Tokenizer** or **MSX Basic Dignified**)  
  
> The *REM tags* can be automatically created by typing `remtags` and pressing TAB on a MSX Basic Dignified syntax page.  
  
### Building  
  
The builds are available from the `Tools > Build System` menu and are called:  
  
`MSX Basic`  
`MSX Basic Dignified`  
  
The build type can be left on `automatic` when using syntax scopes and the extensions of the Basic flavours, Sublime will choose and use the correct one.  
To run the build just press COMMAND-B on Sublime.  
  
When building the Dignified version, by default, the converted, traditional, code will be saved on the same path as the Dignified with an `.asc` extension. A tokenized version will also be saved with a `.bas` extension. **openMSX** will then be opened, mount this folder as a disk and run the `.bas` tokenized version. If no tokenized version was saved, the ASCII `.asc` version will be chosen instead. The execution of the code will then be monitored on **openMSX** and Basic errors will be reported back to Sublime and the correct line will be tagged. A program *Break* will also be reported and direct command errors will generate warnings.  
When using openMSX, Badig Build will try to internally conform the file name to the MSX disk 8 characters and no spaces but some conflict can occur. It is best to always work with 8 characters, no spaces files.  
  
> When using `on error` to catch and customize errors on MSX Basic, always use a `CHR$(7)` (*BEEP*) character and pass the line number as the last text on the error message to make sure the monitoring algorithm will catch and parse the error and its location correctly.  
  
Each of the builds have some variants that can be chosen by pressing COMMAND-SHIFT-B.  
Once they are chosen they will be used as the default COMMAND-B build until Sublime is closed or another variant is chosen. They are:  
  
- MSX Basic Dignified:  
`Default`: Will convert, tokenize, run and monitor the Dignified code.  
`Don't monitor`: Will convert, tokenize and run (but not monitor) the Dignified code.  
`Convert only`: Will convert and tokenize (but not run nor monitor) the Dignified code.  
  
- MSX Basic:  
`Default`: Will only run the traditional Basic code.  
`Tokenize only`: Will only tokenize the traditional Basic code.  
`Tokenize and save list`: Will tokenize the traditional Basic code and save a `.mlt` list file.  
`Tokenize and run`: Will tokenize and run the traditional Basic code.  
  
Arguments passed in `MSX Badig Build.ini` or on *REM tags* will override the default behaviour of the chosen build variant.  
Every build command will open a new instance of **openMSX**.  
  
## Syntax Highlight  
  
Two pretty decent syntax highlights, one for the Dignified version and one for the Classic version of MSX Basic are available.  
  
`MSX Basic Dignified.sublime-syntax`  
```  
name: MSX Basic Dignified  
file_extensions: bad  
scope: source.msxbasicdignified  
```  
###  
`MSX Basic.sublime-syntax`  
```  
name: MSX Basic  
file_extensions: [bas, asc, mlt]  
scope: source.msxbasic  
```  
One of the biggest differences is the Dignified version expects the instructions and variables to be separated by spaces and the Classic accepts them typed together (as per MSX Basic standards).  
The Classic version also has all the Dignified specifics removed for simplicity but maintains useful ones like the labels highlight on its `REM` lines and supports the [**MSX Basic Tokenizer**](https://github.com/farique1/MSX-Basic-Tokenizer) `.mtl` List format.  
  
Both versions side by side:  
![# Versions](https://github.com/farique1/MSX-Sublime-Tools/blob/master/Images/Versions.jpg)  
  
Specifics of the Dignified version:  
![# Highlights](https://github.com/farique1/MSX-Sublime-Tools/blob/master/Images/Highlights.png)  
  
  
1. `REM` scope extends as long as there are line breaks (these lines will be joined together into a single line after the conversion).  
2. The same goes for the `DATA` information; in this case a `_` line break is needed as a `:` denote the end of the instruction.  
3. Quotes explicitly expects a `_` to continue on the next line. MSX Basic support open quotes so a line feed will just end the quote.  
  
MSX Basic Dignified still has issues on some fringe cases so the syntax highlight will try to point some of these potential problems as well as some irregularities that are taken care by the conversion.  
  
4. Leading line numbers are issued automatically so they should not be on the Dignified code; they will be removed automatically with a warning. Numbers beginning a broken `REM` line after a `:`, however, are improperly removed. Both cases are highlighted as a warning.  
5. `ENDIF`s alone on a line are automatically removed on the conversion.  `ENDIF` commands not alone are not removed (will generate a warning) and `ENDIF`s that are part of another command but are alone due to an line break (`_`) are improperly removed. Both cases are highlighted as a warning.  
6. Errors that stop the execution of the conversion are highlighted as errors.  
  
  
## Themes  
  
`MSX Monokai.tmTheme`  
A theme based on Monokai.  
  
`MSX Boxy Ocean.tmTheme`  
A theme based on Boxy Ocean.  
  
They improve the MSX syntax highlight (traditional and Dignified) with scopes specific for the Dignified code: `define`, `declare`, labels, errors and warnings.  
  
` MSX Blue.tmTheme`  
A theme mimicking the blue MSX 1 screen.  
also `MSX Screen 0 New.ttf`.  
An MSX screen 0 TTF font.  
MSX Blue theme and MSX Screen 0 New font on Sublime:  
![# MSX Blue Theme](https://github.com/farique1/MSX-Sublime-Tools/blob/master/Images/BlueTheme.jpg)  
  
## Snippets  
`MSX Basic Dignified.sublime-completions`  
  
Snippets for auto completion of:  
 **FOR-NEXT-STEP**  
 **IF-THEN-ELSE**  
 **LOCATE-PRINT**  
 **Screen initialisation**  
 **FUNC**  
  
`MSX Basic Dignified Remtags.sublime-snippet`  
  
A snippet for the creation of the **Build System** *REM tags*.  
  
## Comment Preference  
  
`MSX Basic Dignified Comments.tmPreferences`  
  
Set `##` as the default comment.  
`##` is a Dignified comment that is deleted when the code is converted to the traditional version.  
There is no block comment but all lines selected will be commented.  
  
There is no Classic comment preference as I couldn't find a way to insert the `REM` or `'` AFTER the line number.  
  
  
## Acknowledgments  
  
As always, all of this is offered as is, with no guaranties whatsoever. Use at your own discretion.  
Having said that, enjoy and send feedback.  
Thanks.  
