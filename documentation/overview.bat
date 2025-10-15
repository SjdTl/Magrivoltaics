@echo off
REM Move to the batch file's directory
cd /d "%~dp0"

REM Run commands

@REM pdflatex overview.tex
dvisvgm overview.pdf --pdf --output=overview.svg 

latexmk -C
svgo overview.svg --pretty
