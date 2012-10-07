// THE BEERWARE LICENSE (Revision 42):
// <thenoviceoof> wrote this file. As long as you retain this notice you
// can do whatever you want with this stuff. If we meet some day, and you
// think this stuff is worth it, you can buy me a beer in return
// - Nathan Hwang (thenoviceoof)

#include <base92.h>
#include <utils.h>

int LEN = 13;

int main() {
        char **strs;
        char *str, *s;
        int i, j;
        
        strs = (char**)malloc(LEN*sizeof(char*));
        strs[0] = "D,";
        strs[1] = "D8*";
        strs[2] = "D81Q";
        strs[3] = "D81RC";
        strs[4] = "D81RPyB";
        strs[5] = "D81RPya(";
        strs[6] = "D81RPya.&";
        strs[7] = "D81RPya.)h";
        strs[8] = "D81RPya.)hg6";
        strs[9] = "D81RPya.)hgN2";
        strs[10] = "D81RPya.)hgNA%";
        strs[11] = "D81RPya.)hgNA($";
        strs[12] = "D81RPya.)hgNA(%s";

        str = (char*)malloc((LEN)*sizeof(char));
        str[0] = 0;

        for(i = 0; i < LEN; i++) {
                printf("MU %d\n", i);
                str[i] = 'a';
                str[i+1] = 0;
                printf("s1: %s\n", base92encode(str, i+1));
                printf("s2: %s\n", strs[i]);
                if(strcmp(base92encode(str, i+1), strs[i]) != 0)
                        exit(1);
                s = base92decode(strs[i], &j);
                printf("s: %s\n", stringify(s, j));
                if(strcmp(stringify(s, j), str) != 0)
                        exit(1);
        }
        return 0;
}
