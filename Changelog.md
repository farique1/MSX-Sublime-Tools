# MSX Sublime Tools  
  
## MSX Badig Build  
  
### **v1.3**  
***18-1-2020***  
- Added tokenize support with the **MSX Basic tokenizer**s  
	- Default behavior now is to tokenize the code both from Dignified and traditional code  
- Added monitoring execution to catch Basic errors when running on the emulator.  
	- Added `-monitor arg`, `##BB:monitor_exec=` and `monitor_exe=` to the `.ini` to enable monitor execution.  
	- Added `openMSXoutput.tcl` TCL script to output **opsnMSX** text responses.  
	- Monitor execution is now the default behaviour  
- Renamed `MSX Badig.sublime-build` to `MSX Basic Dignified.sublime-build`  
	- Added `Don't monitor` option  
- Renamed `MSX Basic Run.sublime-build` to `MSX Basic.sublime-build`  
	- Added `Tokenize only`, `Tokenize and save list` and `Tokenize and run` options  
- Created a more comprehensive `MSX Badig Build.ini` with options: `batoken_filepath = `, `openbatoken_filepath = `, `monitor_exec = `, `throttle = `, `tokenize = `, `tokenize_tool = `, `tokenize_stop = `, `verbose_level = `  
- Updated all log output to the `show_log` function  
- Added verbose levels  
- Verbose level propagate down to called programs  
- Better argument reporting when calling **MSX Basic Dignified**  
- Better **openMSX** log parsing  
- Better general log reporting  
- Code optimizations, improvements and better error check  
  
### **v1.2**  
***9-8-2019***  
- No more savestates, emulator boots with chosen (or default) machine and load disk extension if necessary  
- Extension can be set at slot A or B. Default A.  
- Log output moved to function with more info  
- Settings on Dignified code exclusive rems (##) to override machine and extension  
- Converted file now with .asc extension  
- Better error handling  
  
### **v1.1**  
***5-8-2019***  
- Only call SDL render AFTER loading the file. MUCH faster!  
  
### **v1.0**  
- Initial release.  
  
  
## MSX Basic Dignified.sublime-syntax  
  
  
### **v1.3.1**  
***20-1-2020***  
- Added ##BB:monitor_exec=  
  
### **v1.3**  
***14-1-2020***  
- Added FUNC proto-function definition and calling  
- Added FN function name highlight  
  
### **v1.2**  
***18-9-2019***  
- Added &O  
- Added OUTPUT  
- Added AS  
- Added True and False  
- Added INCLUDE  
- Added support for scientific notation  
- Added operator scope to &H &O &B with  
- Added operator scope to variable and numeric types $%!# and preceding #  
- Improved DECLARE with new long var rules  
- Improved DECLARE must be followed by space, DEFINE don't  
- Improved Dignified commands highlight  
- Improved Highlight for the build settings tags (##BB:)  
- Improved exclusive comment (##) separating from ' and REM.  
- Improved CALL and subsequent 15 char string  
- Improved DEFUSR e USR() highlight word and number, i.e.: DEFUSR1  
- Improved DATA ## and _ handling  
- Fixed instructions highlighting inside variable name  
  
### **v1.1**  
- Not registered.  
  
### **v1.0**  
- Initial release.  
  
  
  
## MSX Basic.sublime-syntax  
  
### **v1.3**  
***14-1-2020***  
- Added FN function name highlight  
- Fixed ASC being superseeded by AS  
  
### **v1.2**  
***18-9-2019***  
- Added &O  
- Added OUTPUT  
- Added AS  
- Added operator scope to &H &O &B with  
- Added operator scope to variable and numeric types $%!# and preceding #  
- Added .asc extension  
- Added .mlt extension (List file for the MSX Basic Tokenizer)  
- Added support for Tokenizer's List syntax  
- Added support for scientific notation  
- Added Support for <= and >= ligatures  
- Improved CALL and subsequent 15 char string  
- Improved DEFUSR e USR() highlight word and number, i.e.: DEFUSR1  
- Fixed highlight KEY as instruction after line numbers  
  
### **v1.1**  
- Not registered.  
  
### **v1.0**  
- Initial release.  
  
  
## MSX Sublime Tools misc files.  
  
### **v1.4**  
***23-1-2020***  
  
Created files:  
- `MSX Basic Dignified Remtags.sublime-snippet`  
	- Snippet for the Dignified *REM tags*  
- `MSX Basic Dignified.sublime-completions`  
	- Autocompletion for the Dignified Basic  
- `MSX Blue.tmTheme`  
	- Theme mimicking the MSX 1 blue screen  
- `MSX Screen 0 New.ttf`  
	- TTF font emulating the screen 0 MSX font  
  
Names changed:  
- `MSX Comments.tmPreferences` to `MSX Basic Dignified Comments.tmPreferences`  
