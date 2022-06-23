anfang:
CLS
x=l:y=l

Start:
IF y>10 THEN
    IF y>23 THEN
        GOTO anfang
    ELSEIF x>80 THEN
        PRINT :y=y+l:x=l
    ELSE
        PRINT "#";:x=x+l
    END IF

ELSEIF y<ll THEN
    IF x>80 THEN
        PRINT :y=y+l :x=l
    ELSEIF x>20 THEN
        PRINT "#":x=x+l
    ELSE
        PRINT " ";:x=x+l
    END IF
END IF
GOTO start