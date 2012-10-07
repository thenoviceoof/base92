// THE BEERWARE LICENSE (Revision 42):
// <thenoviceoof> wrote this file. As long as you retain this notice you
// can do whatever you want with this stuff. If we meet some day, and you
// think this stuff is worth it, you can buy me a beer in return
// - Nathan Hwang (thenoviceoof)

#include <base92.h>

#include <stdio.h>

unsigned char ENCODE_MAPPING[256] = (unsigned char[]){
        33, 35, 36, 37, 38, 39, 40, 41, 42, 43,
        44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
        54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
        64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
        74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
        84, 85, 86, 87, 88, 89, 90, 91, 92, 93,
        94, 95, 97, 98, 99, 100, 101, 102, 103, 104,
        105, 106, 107, 108, 109, 110, 111, 112, 113, 114,
        115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
        125, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0
};
unsigned char DECODE_MAPPING[256] = (unsigned char[]){
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 0, 255, 1, 2, 3, 4, 5,
        6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
        26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
        36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
        46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
        56, 57, 58, 59, 60, 61, 255, 62, 63, 64,
        65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
        75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
        85, 86, 87, 88, 89, 90, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
        255, 255, 255, 255, 255, 255
};

unsigned char base92chr_encode(unsigned char byt) {
        return ENCODE_MAPPING[byt];
}

unsigned char base92chr_decode(unsigned char byt) {
        return DECODE_MAPPING[byt];
}

unsigned char* base92encode(unsigned char* str, int len) {
        unsigned int i, j;       // i for raw, j for encoded
        unsigned int size;       // for the malloc
        unsigned long workspace; // bits holding bin
        unsigned short wssize;   // number of good bits in workspace
        int tmp;
        unsigned char c;
        unsigned char *res;
        
        if (len == 0) {
                return "~";
        }
        // precalculate how much space we need to malloc
        size = (len * 8) % 13;
        if (size == 0) {
                size = 2 * ((len * 8) / 13);
        } else if (size < 7) {
                size = 2 * ((len * 8) / 13) + 1;
        } else {
                size = 2 * ((len * 8) / 13) + 2;
        }
        printf("size: %d\n", size);
        // do the malloc, add space for a null byte
        res = (char*)malloc(sizeof(char) * (size + 1));
        workspace = 0;
        wssize = 0;
        j = 0;
        for (i = 0; i < len; i++) {
                printf("i: %d, j: %d\n", i, j);
                workspace = workspace << 8 | str[i];
                wssize += 8;
                if (wssize >= 13) {
                        tmp = (workspace >> (wssize - 13)) & 8191;
                        c = base92chr_encode(tmp / 91);
                        if (c == 0) {
                                // do something, illegal character
                                free(res);
                                return NULL;
                        }
                        res[j++] = c;
                        c = base92chr_encode(tmp % 91);
                        if (c == 0) {
                                // do something, illegal character
                                free(res);
                                return NULL;
                        }
                        res[j++] = c;
                        wssize -= 13;
                }
        }
        // encode a last byte
        if (0 < wssize && wssize < 7) {
                tmp = (workspace << (6 - wssize)) & 63;  // pad the right side
                c = base92chr_encode(tmp);
                if (c == 0) {
                        // do something, illegal character
                        free(res);
                        return NULL;
                }
                res[j] = c;
        } else if (7 <= wssize) {
                tmp = (workspace << (13 - wssize)) & 8191; // pad the right side
                c = base92chr_encode(tmp / 91);
                if (c == 0) {
                        // do something, illegal character
                        free(res);
                        return NULL;
                }
                res[j++] = c;
                c = base92chr_encode(tmp % 91);
                if (c == 0) {
                        // do something, illegal character
                        free(res);
                        return NULL;
                }
                res[j] = c;
        }
        // add the null byte
        res[size] = 0;
        return res;
}

unsigned char* base92decode(unsigned char* str) {
        return "";
}
