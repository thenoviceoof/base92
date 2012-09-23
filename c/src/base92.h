// THE BEERWARE LICENSE (Revision 42):
// <thenoviceoof> wrote this file. As long as you retain this notice you
// can do whatever you want with this stuff. If we meet some day, and you
// think this stuff is worth it, you can buy me a beer in return
// - Nathan Hwang (thenoviceoof)

// check if the header has been included before
#ifndef BASE92
#define BASE92

#include <stdlib.h>
#include <string.h>

char base92chr_encode(char byt);

char base92chr_decode(char byt);

char* base92encode(char* str);

char* base92decode(char* str);

#endif
