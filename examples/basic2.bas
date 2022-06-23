EinlesenDefinitionsbereich:

REM INPUT "x Min";xl
REM INPUT "x Max";xr
REM INPUT "y Min";yh
REM INPUT "y Max";yv
REM INPUT "z Min";zu
REM INPUT "z Max";zo
REM PRINT "Eingabe Korrekt ? (j/n)"

Korrektheit:

eg$ = INKEY$
REM IF eg$ = "n" THEN GOTO EinlesenDefinitionsbereich
REM IF eg$ <> "j" THEN GOTO Korrektheit

Grafikbildschirmeinschalten:

SCREEN 2,640,400,2,2
WINDOW 2

Polyedereckpunkte:

xl = 1
xr = 5
yh = 1
yv = 5
zu = 1
zo = 5

dx = (xr-xl)/408
dy = (yv-yh)/66
zd = zo-zu:dz = zd/133:z0 = zo/dz
x1 = 231: x2 = 631

