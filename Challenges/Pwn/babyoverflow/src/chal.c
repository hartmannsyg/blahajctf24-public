//compile: gcc chal.c -fstack-protector -no-pie -o chal
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
 
void win(){
    printf("You win! Here is flag: blahaj{4ctuAlLy_UnD3rFl0w}\n");
}

int main(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    int changeme = 0;
    char i = 0;
    int count = 0;
    char buffer[1024];
    printf("Type your note: ");
    fflush(stdout);
    while(1){
        if(count >= 1024){
            printf("Go away hacker!!!\n");
            exit(0);
        }else if(changeme == 0x1337beef){
            win();
            exit(0);
        }else{
            read(fileno(stdin), &i, 1);
            if(i == 0x8){
                count--;
                printf("\b");
            }else{
                buffer[count] = i;
                count++;
            }
        }
    }
}