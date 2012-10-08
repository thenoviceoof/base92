// THE BEERWARE LICENSE (Revision 42):
// <thenoviceoof> wrote this file. As long as you retain this notice you
// can do whatever you want with this stuff. If we meet some day, and you
// think this stuff is worth it, you can buy me a beer in return
// - Nathan Hwang (thenoviceoof)

#include <stdlib.h>

unsigned char *stringify(char *str, int i) {
        int j;
        unsigned char *s;
        
        s = (unsigned char*)malloc(sizeof(char) * i + 1);
        for (j = 0; j < i; j++) {
                s[j] = str[j];
        }
        s[j+1] = 0;
        return s;
}
