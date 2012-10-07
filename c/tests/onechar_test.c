// THE BEERWARE LICENSE (Revision 42):
// <thenoviceoof> wrote this file. As long as you retain this notice you
// can do whatever you want with this stuff. If we meet some day, and you
// think this stuff is worth it, you can buy me a beer in return
// - Nathan Hwang (thenoviceoof)

#include <base92.h>

int main() {
        int i;
        char *str = "A";

        if(strcmp(base92encode(str, 1), "8q") != 0)
                exit(1);
        if(base92decode("8q", &i)[0] != 'A')
                exit(1);
        return 0;
}
