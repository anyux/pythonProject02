@echo off
set str=superhero
echo str=%str%
echo str:~0,5=%str:~0,5%
echo str:~3=%str:~3%
echo str:~-3=%str:~-3%
echo str:~0,-3=%str:~0,-3%
pause

@echo off
set str=hello world!
set temp=%str:hello=good%
echo %temp%
pause