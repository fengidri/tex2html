/**
 *   author       :   丁雪峰
 *   time         :   2015-07-29 18:16:32
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :
 */
#include <stdio.h>
#include <stddef.h>
#include <unistd.h>

#include "units.h"


bool is_en(char c)
{
    switch(c)
    {
        case ' ':
        case '\n':
        case '#':
        case '$':
        case '^':
        case '&':
        case '_':
        case '{':
        case '}':
        case '~':
            return false;
        default:
            return true;
    }
}

char *skip_to_lf(char *p)
{
    while(1)
    {
        if (*p == 0) return  NULL;
        if (*p == '\n') return p;
        p += 1;
    }
}
char *skip_space(char *p)
{
    while(1)
    {
        if (*p == 0) return  NULL;
        if (*p != ' ') return p;
        p += 1;
    }
}

bool is_tex(char c)
{
    switch(c)
    {
        case '#':
        case '$':
        case '%':
        case '^':
        case '&':
        case '_':
        case '{':
        case '}':
        case '~':
        case '\\':
            return false;
        default:
            return true;
    }
}

bool is_letter(char c)
{
    if (c >= 'A' && c <= 'Z') return true;
    if (c >= 'a' && c <= 'z') return true;
    return false;
}
