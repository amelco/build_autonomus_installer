@echo off
echo Inicializando Autonomus...

cd %programfiles(x86)%\LAIS\Autonomus\autonomus-socket

start /min autonomus-socket-win.exe

cd %programfiles(x86)%\LAIS\Autonomus\build
start /min build.exe

::Espera por 3 segundos até inicializar o build.exe
PING localhost -n 3 >NUL

cd %programfiles(x86)%\LAIS\Autonomus\win-unpacked
start autonomus.exe

echo Concluído!
