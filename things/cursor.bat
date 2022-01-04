@echo off
rem i have no idea how this works. i copied it from stackoverflow kekw
set a1=%1
for /F "delims=#" %%h in ('prompt #$E# ^& for %%h in ^(1^) do rem') do set esc=%%h
if %a1%==0 goto off
if %a1%==1 goto on
goto exit
:off
echo.%esc%[?25l
goto exit
:on
echo.%esc%[?25h
goto exit
:exit