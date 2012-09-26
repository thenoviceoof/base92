// THE BEERWARE LICENSE (Revision 42):
// <thenoviceoof> wrote this file. As long as you retain this notice you
// can do whatever you want with this stuff. If we meet some day, and you
// think this stuff is worth it, you can buy me a beer in return
// - Nathan Hwang (thenoviceoof)

#include <base92.h>

int main() {
        if(base92chr_encode(0) != '!')
                exit(1);
        if(base92chr_encode(1) != '#')
                exit(1);
        if(base92chr_encode(61) != '_')
                exit(1);
        if(base92chr_encode(62) != 'a')
                exit(1);
        if(base92chr_encode(90) != '}')
                exit(1);
        if(base92chr_encode(91) != 0)
                exit(1);
        return 0;
}
