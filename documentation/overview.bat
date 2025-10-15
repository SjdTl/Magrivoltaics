@echo off
REM Move to the batch file's directory
cd /d "%~dp0"

REM Run commands
dvisvgm --pdf overview.pdf
latexmk -C
svgo overview.svg --pretty
