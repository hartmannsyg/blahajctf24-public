//gcc chal.c -fstack-protector -no-pie -o chal
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
void win(){
    system("cat flag.txt");
}
int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    char leet[10] = {0};
    puts("What is your name?");
    read(0, stdin, 480);
    puts("Are you 1337?");
    fgets(leet, 9, stdin);
    puts("You are not 1337.");
}