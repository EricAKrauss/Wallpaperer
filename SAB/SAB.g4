grammar SAB;

//s : head | (head ('\n' s)) | ;
s: head (NEWLINE head)* END;
head : (slideshow | group | overlay_text | overlay_image | source)';';

source : SOURCE ' ' variable ' ' path;
group : GROUP ' ' variable ':'NEWLINE DIGIT ' ' path image (NEWLINE DIGIT ' ' path image)*;

overlay_image : OVERLAY ' IMAGE ' variable ':'NEWLINE path image NEWLINE position;
overlay_text : OVERLAY ' TEXT ' variable ':'NEWLINE command position;
command : COMMAND ' ' path script NEWLINE;
position : (RIGHT | LEFT) ' ' PERCENT NEWLINE (TOP | BOTTOM) ' ' PERCENT NEWLINE JUSTIFY ' ' justified_pos;
justified_pos : (RIGHT | LEFT);

slideshow : SLIDESHOW ' ' variable ':'NEWLINE slidesource slidetime slideorder;
slidesource : (DIGIT ' ' variable NEWLINE)+;
slidetime : TIME ' ' DIGIT+ ' ' timetype NEWLINE;
slideorder : ORDER ' '(SHUFFLE | ALPHABETICAL);
timetype : (SECOND|MINUTE|HOUR);


path : '/'variable (path | '/' | );
image : variable '.' ('png' | 'jpg' | 'jpeg' | 'bmp' );
script : variable '.sh';
variable : LETTER(DIGIT|LETTER|'-'|'_')*;

PERCENT : ('0'..'9')+ '%';
DIGIT : '0'..'9';
LETTER : ('a'..'z' |  'A'..'Z');

NEWLINE : ('\n'|'\r'|'\r\n')+ ('\t'|' ')*;
SOURCE : 'SOURCE';
SLIDESHOW : 'SLIDESHOW';
OVERLAY : 'OVERLAY';
GROUP : 'GROUP';
COMMAND : 'COMMAND';
JUSTIFY : 'JUSTIFY';

TIME : 'TIME';
SECOND : 'SECONDS'|'SECOND';
MINUTE : 'MINUTES'|'MINUTE';
HOUR   : 'HOURS'  |'HOUR';
ORDER : 'ORDER';
SHUFFLE : 'SHUFFLE';
ALPHABETICAL : 'ALPHABETICAL';

RIGHT : 'RIGHT';
LEFT  : 'LEFT';
TOP   : 'TOP';
BOTTOM: 'BOTTOM';

END   : NEWLINE? ';' ;


