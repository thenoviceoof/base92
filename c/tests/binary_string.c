// THE BEERWARE LICENSE (Revision 42):
// <thenoviceoof> wrote this file. As long as you retain this notice you
// can do whatever you want with this stuff. If we meet some day, and you
// think this stuff is worth it, you can buy me a beer in return
// - Nathan Hwang (thenoviceoof)

#include <base92.h>

int main() {
        char *str = (char*)malloc(16*sizeof(char));
        str[0] = 182;
        str[1] = 59;
        str[2] = 187;
        str[3] = 224;
        str[4] = 30;
        str[5] = 238;
        str[6] = 208;
        str[7] = 147;
        str[8] = 203;
        str[9] = 34;
        str[10] = 187;
        str[11] = 143;
        str[12] = 90;
        str[13] = 205;
        str[14] = 195;
        str[15] = 0;
        if(strcmp(base92encode(str, 15), "c)L#O2K}%8Vo_OM3kB:") != 0)
                exit(1);
        if(strcmp(base92decode("c)L#O2K}%8Vo_OM3kB:"), str) != 0)
                exit(1);
        return 0;
}
