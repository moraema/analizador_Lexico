%{
#include <stdio.h>
#include <stdlib.h>
%}

DIGITO  [0-9]
LETRA   [a-zA-Z_]
ESPACIO [ \t]+
NUMERO  {DIGITO}+
FLOTANTE {NUMERO}"."{NUMERO}
VARIABLE {LETRA}({LETRA}|{DIGITO})*
OPERADOR [\+\-\*\/]
COMPARACION "<="|">="|"=="|"!="|"<"|">"
ASIGNACION "="
SEPARADOR ";"
DELIMITADOR "("|")"|"{"|"}"
DOS_PUNTOS ":"
PUNTO "\."
LOGICO  &&"|"||"|"!"
COMILLAS \"[^\"]*\"
COMENTARIO "/\*".*"\*/"

%%
"if"       { printf("TOKEN_IF\n"); return IF; }
"else"     { printf("TOKEN_ELSE\n"); return ELSE; }
"while"    { printf("TOKEN_WHILE\n"); return WHILE; }
"for"      { printf("TOKEN_FOR\n"); return FOR; }
"escribir" { printf("TOKEN_ESCRIBIR\n"); return ESCRIBIR; }
"leer"     { printf("TOKEN_LEER\n"); return LEER; }
"val"      { printf("TOKEN_VAL\n"); return VAL; }
"init"     { printf("TOKEN_INIT\n"); return INIT; }
"func"     { printf("TOKEN_FUNC\n"); return FUNC; }

{FLOTANTE}    { printf("TOKEN_FLOTANTE: %s\n"); return FLOTANTE; }
{NUMERO}      { printf("TOKEN_ENTERO: %s\n"); return ENTERO; }
{VARIABLE}    { printf("TOKEN_VARIABLE: %s\n"); return VARIABLE; }
{OPERADOR}    { printf("TOKEN_OPERADOR: %s\n"); return OPERADOR; }
{COMPARACION} { printf("TOKEN_COMPARACION: %s\n"); return COMPARACION; }
{ASIGNACION}  { printf("TOKEN_ASIGNACION: %s\n"); return ASIGNACION; }
{SEPARADOR}   { printf("TOKEN_SEPARADOR\n"); return SEPARADOR; }
{DELIMITADOR} { printf("TOKEN_DELIMITADOR: %s\n"); return DELIMITADOR; }
{DOS_PUNTOS}  { printf("TOKEN_DOS_PUNTOS\n"); return DOS_PUNTOS; }
{PUNTO}       { printf("TOKEN_PUNTO\n"); return PUNTO; }
{LOGICO}      { printf("TOKEN_LOGICO\n"); return LOGICO; }
{COMILLAS}    { printf("TOKEN_COMILLAS: %s\n"); return COMILLAS; }
{COMENTARIO}  { /* Ignorar comentarios */ }

{ESPACIO}     { /* Ignorar espacios y tabulaciones */ }

\n            { /* Contar líneas si es necesario */ }

.             { printf("Caracter desconocido: %s\n", yytext); }

%%
int main() {
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}
