// THE BEERWARE LICENSE (Revision 42):
// <thenoviceoof> wrote this file. As long as you retain this notice you
// can do whatever you want with this stuff. If we meet some day, and you
// think this stuff is worth it, you can buy me a beer in return
// - Nathan Hwang (thenoviceoof)

#include <base92.h>

int main() {
        if(strcmp(base92encode(""), "~") != 0)
                exit(1);
        if(strcmp(base92decode(""), "") != 0)
                exit(1);
        return 0;
}
