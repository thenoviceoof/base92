// THE BEERWARE LICENSE (Revision 42):
// <thenoviceoof> wrote this file. As long as you retain this notice you
// can do whatever you want with this stuff. If we meet some day, and you
// think this stuff is worth it, you can buy me a beer in return
// - Nathan Hwang (thenoviceoof)

#include <base92.h>
#include <utils.h>

int main() {
        int i;
        char* s;
        if(strcmp((char*)base92encode((unsigned char*)"hello world", 11), "Fc_$aOTdKnsM*k") != 0)
                exit(1);
        s = (char*)base92decode((unsigned char*)"Fc_$aOTdKnsM*k", &i);
        if(strcmp(stringify(s, i), "hello world") != 0)
                exit(1);
        return 0;
}
