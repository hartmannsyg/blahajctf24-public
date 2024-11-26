// gcc chal.c -O0 -Wl,-z,relro,-z,now -s
#include <stdio.h>
#include <stdlib.h>
int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    printf("Surely a single overflow can't be that bad... right?\nPlease enter size of your malloc: ");
    unsigned int malsz = 0;
    scanf("%d", &malsz);
    unsigned char *alloc = malloc(malsz);
    printf("Cool, you got an alloc to %p\nNow, please select your offset: ", alloc);
    unsigned int off = 0;
    scanf("%d", &off);
    printf("And pray tell, what would you wish to write to there?\n");
    unsigned long long datum = 0;
    scanf("%lld", &datum);
    *((unsigned long long*)(alloc + off)) = datum;
    puts(NULL); //i find that a segfault is the safest way to exit... we don't want people screwing with exit handlers now do we?
}