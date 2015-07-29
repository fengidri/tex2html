/**
 *   author       :   丁雪峰
 *   time         :   2015-07-29 16:45:41
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :
 */
#include <stdio.h>
#include <stddef.h>
#include <unistd.h>
#include <stdbool.h>

#include "units.h"



typedef enum{
    TYPE_CONTROL,   // 控制序列
    TYPE_CONPUC,    // 形如\# \$ \% \^ \& \_ \{ \} \~
    TYPE_TEXPUNC,   // # $ %
    TYPE_TEXT_CN,
    TYPE_TEXT_EN,
    TYPE_TEXT_PUNC, // , . ! "
    TYPE_UNKNOW,
}TYPE;


TYPE get_token(char *p, int *len)
{
    int l = 1;

    if ('\\' == *p) {
        if (1 == l)
        {
            if (is_tex(*(p + l)))
            {
                *len = 2;
                return TYPE_TEXPUNC;
            }
            if (!is_letter(*(p + 1)))
            {
                return TYPE_UNKNOW;
            }
        }
        while(1)
        {
            if (is_letter(*(p + l)))
            {
                l ++;
                continue;
            }
            *len = l;
            return TYPE_CONTROL;
        }
    }
    if ('%' == *p)
    {
        skip_to_lf()
    }

}



















