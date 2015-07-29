/**
 *   author       :   丁雪峰
 *   time         :   2015-07-29 18:16:51
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :
 */
#ifndef  __UNITS_H__
#define __UNITS_H__
#include <stdbool.h>

bool is_en(char c);
char *skip_to_lf(char *p);
char *skip_space(char *p);
bool is_tex(char c);
bool is_letter(char c);
#endif


