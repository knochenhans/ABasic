Anfang:
PRINT "Videotitel-Programm "
PRINT "von Franz Maier"
PRINT

Auswahl:
PRINT "Auswahl:"
PRINT "1 Text eingeben"
PRINT "2 Objects einlesen"
PRINT "3 Obj.Bewegung festlegen"
PRINT "4 Farben festlegen"
PRINT "5 Titel wiedergeben"
PRINT

Abfrage:
LOCATE 10,1
PRINT "Ihre Wahl:";
INPUT a$

REM GOTO Auswahl

# REM Menüsteuerung - sehr einfach
# MENU 1,0,1,"Menü 1"
# MENU 2,0,1,"Menü 2"
# FOR i = 1703
# MENU 1,i,1,"Punkt 1."+CHRS(48+i)
# MENU 2,i,1,"Punkt 2."+CHRS(48+I)
# NEXT i
# MENU 1,4,1,"Beenden"
# ende = 0
# ON MENU GOSUB Wahl
# MENU ON
# WHILE ende = 0 : WEND
# MENU RESET
# END

# Wahl:
# 	m% = MENU(0) : p% = MENU(1)
# 	LOCATE 10,1
# 	PRINT "Menü "+CHRS(48+m%)

# PRINT "Punkt "+CHRS(48+p%)

# IF m% = 1 AND p% = 4 THEN ende = 1
# RETURN