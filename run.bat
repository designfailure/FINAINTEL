@echo off

:: Aktiviraj virtualno okolje
call venv\Scripts\activate.bat

:: Zaženi aplikacijo
python workspace.py %* 