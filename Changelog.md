# MSX Basic Dignified.sublime-syntax
## **v1.2**  

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

## **v1.1**  
- Not registered.  

## **v1.0**  
- Initial release.  



# MSX Basic.sublime-syntax
## **v1.2**  

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

## **v1.1**  
- Not registered.  

## **v1.0**  
- Initial release.  

# MSX Badig Build.py
## **v1.2**  

***9-8-2019***  
- No more savestates, emulator boots with chosen (or default) machine and load disk extension if necessary
- Extension can be set at slot A or B. Default A.
- Log output moved to function with more info
- Settings on Dignified code exclusive rems (##) to override machine and extension
- Converted file now with .asc extension
- Better error handling

## **v1.1**  
***5-8-2019***
- Only call SDL render AFTER loading the file. MUCH faster!  

## **v1.0**  
- Initial release.  
