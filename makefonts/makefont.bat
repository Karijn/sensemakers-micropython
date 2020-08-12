@echo off

if "%2" == "" goto nofont

if "%3" == "" goto noargs

echo %1 %2 %3
font_to_py.py %1 %2 %3
goto end

:nofont
rem call %0 RobotoCondensed-Regular.ttf roboto_cond_reg
rem rshell -p com4
call %0 OpenSans-Regular.ttf opensans
call %0 FreeSans.ttf freesans
call %0 FreeSansBold.ttf free_sans_bold
call %0 FreeSansBoldOblique.ttf free_sans_oblique
call %0 FreeSansOblique.ttf free_sans_bold_oblique

pause
goto end

:noargs
call %0 %1 12 ..\fonts\%2_12.py
call %0 %1 16 ..\fonts\%2_16.py
call %0 %1 20 ..\fonts\%2_20.py
call %0 %1 24 ..\fonts\%2_24.py
call %0 %1 30 ..\fonts\%2_30.py
call %0 %1 36 ..\fonts\%2_36.py
:end


