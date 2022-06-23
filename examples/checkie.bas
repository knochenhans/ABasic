REM * Checkie42_Deluxe von Marius Chwalczyk, 1991 *
DEFINT a-z
REM * Vom Benutzer nach Wunsch zu ändern *
    path$="sys:"
    unit$="DFO: "+"DF1: "+"DHO: "+"RAM: "
    datasnr=10
    skip=3
REM * * *
ON ERROR GOTO EndIt
ON BREAK GOSUB BreakIt
BREAK ON
LIBRARY "dos.library"
LIBRARY "exec.library"
LIBRARY "graphics.library"
DECLARE FUNCTION Examine LIBRARY
DECLARE FUNCTION ExNext LIBRARY
DECLARE FUNCTION Lock& LIBRARY
DECLARE FUNCTION AllocMem& LIBRARY
WINDOW 1," Checkie42 Deluxe von Marius Chwalezyk ",(11,11)-(618,78),22
REM rp&=WINDOW(8):
LINE (0,0)-(607,10),,b
LINE (443,0)-(531,10),,b:LINE (11,19)-(60,36),,b
LINE (11,43)-(60,60),,b:LINE (74,19)-(596,60),,b
mt=1:mp=0:READ i

WHILE i<>-1
    WHILE i<>-1:READ txt$:MENU mt,mp,i,txt$:mp=mp+1:READ i:WEND
    mt=mt+1:mp=0:READ i
WEND
DATA 1,Datei, 1, "Neu...       ", 1, "Öffnen...    ", 1, "Anfügen...   ", 0, "...Schließen "
DATA          1, "Anzeigen...  ", 1, "Drucken...   ", 1, "Ende         ", -1
DATA 0,Gehe zu, 1, "Zeile...", 1, "Anfang  ", 1, "Ende   ", -1
DATA 0,Ändern, 1, "Checksumme ändern F1", 1, "Checks. berechnen F6", 1, "Zurück            F3"
DATA 1, "Großschreibung      ", -1
DATA 1,0ptionen, 2,"   Einfügen  ", 1,"   DATA-Zeile", 1, "   Einrücken ", -1, -1